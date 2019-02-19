from datetime import date
from datetime import timedelta
from django.forms import ModelForm
from django.forms import CheckboxSelectMultiple
from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.views import generic
from io import BytesIO
from urllib.parse import urlencode
from wkhtmltopdf.views import PDFTemplateView
from zipfile import ZipFile
from .models import Employee
from .models import Event
from .models import EventDate


EVENT_FIELDS = [
    'title',
    'room',
    'sound_type',
    'ba',
    'rider',
    'folder',
    'additional_info',
]


class VapleForm(ModelForm):
    def extra_classes(self, name):
        classes = []
        if name in self.instance.fields_wanted():
            classes.append('wanted')
        return classes

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class(bf.errors)
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes(
                    extra_classes=self.extra_classes(name))
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))

                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': bf_errors,
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'css_classes': '',
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))

    def as_table_row(self):
        "Return this form rendered as HTML <td>s."
        return self._html_output(
            normal_row='<td%(html_class_attr)s>%(errors)s%(field)s%(help_text)s</td>',
            error_row='<td>%s</td>',
            row_ender='</td>',
            help_text_html='<span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )

    def as_spans(self):
        "Return this form rendered as HTML <td>s."
        return self._html_output(
            normal_row='<span%(html_class_attr)s>%(errors)s%(field)s%(help_text)s</span>',
            error_row='<span>%s</span>',
            row_ender='</span>',
            help_text_html='<span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )


class EventForm(VapleForm):
    class Meta:
        model = Event
        fields = EVENT_FIELDS


class EventDateForm(VapleForm):
    class Meta:
        model = EventDate
        fields = ['employees']
        widgets = {
            'employees': CheckboxSelectMultiple(),
        }


class EventOverview(generic.list.ListView):

    model = EventDate
    template_name = 'vaple_core/event_list.html'
    paginate_by = 50
    show_orphans = True

    def add_months(self, basedate, num_months=1):
        return basedate.replace(month=(basedate.month + num_months) % 12)

    def get_month_range(self, basedate):
        date_from = date(year=basedate.year, month=basedate.month, day=1)
        next_month = self.add_months(date_from)
        date_to = next_month - timedelta(days=1)
        return date_from, date_to

    @property
    def current_month(self):
        today = date.today()
        return self.get_month_range(today)

    @property
    def date_from(self):
        current_month = self.current_month
        date_from_iso = self.request.GET.get('from')
        if date_from_iso:
            date_from = date.fromisoformat(date_from_iso)
        else:
            date_from = current_month[0]
        return date_from

    @property
    def date_to(self):
        current_month = self.current_month
        date_to_iso = self.request.GET.get('to')
        if date_to_iso:
            date_to = date.fromisoformat(date_to_iso)
        else:
            date_to = current_month[1]
        return date_to

    def quicklinks(self):
        quicklinks = []
        current_month = self.current_month
        quicklinks.append(
            {
                'date_from': current_month[0],
                'date_to': current_month[1],
                'title': current_month[0].strftime('%B'),
            }
        )
        for n in range(1, 4):
            basedate = self.add_months(current_month[0], num_months=n)
            date_from, date_to = self.get_month_range(basedate)
            quicklinks.append(
                {
                    'date_from': date_from,
                    'date_to': date_to,
                    'title': date_from.strftime('%B'),
                }
            )
        return quicklinks

    def _get_queryset(self):
        date_from = self.date_from
        date_to = self.date_to
        queryset = self.model._default_manager.order_by('date')
        if date_from:
            queryset = queryset.filter(date__gt=date_from)
        if date_to:
            queryset = queryset.filter(date__lt=date_to)
        return queryset

    def get_queryset(self):
        return [
            (
                eventdate,
                eventdate.event,
                EventDateForm(instance=eventdate),
                EventForm(instance=eventdate.event),
            ) for eventdate in self._get_queryset()
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_names'] = [
            Event._meta.get_field(field).verbose_name
            for field in EVENT_FIELDS]
        context['orphans'] = [
            (
                event,
                EventForm(instance=event),
            ) for event in Event.objects.filter(eventdate=None)
        ]
        context['date_from'] = self.date_from
        context['date_to'] = self.date_to
        context['quicklinks'] = self.quicklinks
        context['show_orphans'] = self.show_orphans
        return context


class EventOverviewExport(EventOverview, PDFTemplateView):

    filename = 'export-full.pdf'
    cmd_options = {
        'orientation': 'Landscape',
    }
    show_orphans = False

    def get(self, request, *args, **kwargs):
        return EventOverview.get(self, request, *args, **kwargs)


class EmployeeExport(EventOverviewExport):

    @property
    def filename(self):
        filename = '{name}-{date_from}_{date_to}.pdf'.format(
            name=Employee.objects.get(pk=self.kwargs['pk']).name,
            date_from=self.date_from.isoformat(),
            date_to=self.date_to.isoformat(),
        )
        return filename

    def _get_queryset(self):
        queryset = super(EmployeeExport, self)._get_queryset()
        queryset = queryset.filter(employees=self.kwargs['pk'])
        return queryset

def batch_employee_export(request):
    stream = BytesIO()
    zipped = ZipFile(stream, 'w')
    for employee in Employee.objects.all():
        view = EmployeeExport.as_view()(request, pk=employee.pk)
        zipped.writestr(view.filename, view.rendered_content)
    zipped.close()
    stream.seek(0)
    return FileResponse(
        streaming_content=stream,
        as_attachment=True,
        filename='batch_employee_export-{date_from}_{date_to}.zip'.format(
            date_from=request.GET.get('from'),
            date_to=request.GET.get('to'),
        ),
        content_type='application/zip',
    )

class RedirectToIndex(object):

    @property
    def success_url(self):
        url = reverse_lazy(
            'vaple_core:index',
        )
        query = {}
        query['from'] = self.request.POST.get('from')
        query['to'] = self.request.POST.get('to')
        query = {key: value for key, value in query.items() if value}
        querystr = urlencode(query)
        if querystr:
            url = '{url}?{querystr}'.format(url=url, querystr=querystr)
        return url


class EventCreate(RedirectToIndex, generic.edit.CreateView):
    model = Event
    fields = EVENT_FIELDS
    title = 'Veranstaltung hinzufügen'


class EventUpdate(RedirectToIndex, generic.edit.UpdateView):
    model = Event
    fields = EVENT_FIELDS
    title = 'Veranstaltung bearbeiten'


class EventDelete(RedirectToIndex, generic.edit.DeleteView):
    model = Event
    title = 'Veranstaltung löschen'


class EventDateCreate(RedirectToIndex, generic.edit.CreateView):
    model = EventDate
    fields = [
        'date',
        'event',
    ]
    title = 'Datum hinzufügen'


class EventDateUpdate(RedirectToIndex, generic.edit.UpdateView):
    model = EventDate
    fields = [
        'date',
        'employees',
    ]
    title = 'Datum bearbeiten'


class EventDateList(generic.list.ListView):
    model = EventDate

    def get_queryset(self, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        return event.eventdate_set.order_by('date')

    def get_context_data(self, **kwargs):
        context = super(EventDateList, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.kwargs['pk'])
        context['today'] = date.today().isoformat()
        return context


class EventDateDelete(RedirectToIndex, generic.edit.DeleteView):
    model = EventDate
    template_name_suffix = '_form'
