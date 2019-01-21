from datetime import date
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.views import generic
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
    'employees',
]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = EVENT_FIELDS

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


class EventOverview(generic.list.ListView):
    model = EventDate
    template_name = 'vaple_core/event_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model._default_manager.order_by('date')
        return [
            (
                eventdate,
                eventdate.event,
                EventForm(instance=eventdate.event),
            ) for eventdate in queryset
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
        return context


class EventCreate(generic.edit.CreateView):
    model = Event
    fields = EVENT_FIELDS
    success_url = reverse_lazy('vaple_core:index')
    title = 'Veranstaltung hinzufügen'


class EventUpdate(generic.edit.UpdateView):
    model = Event
    fields = EVENT_FIELDS
    success_url = reverse_lazy('vaple_core:index')
    title = 'Veranstaltung bearbeiten'


class EventDelete(generic.edit.DeleteView):
    model = Event
    success_url = reverse_lazy('vaple_core:index')
    title = 'Veranstaltung löschen'


class EventDateCreate(generic.edit.CreateView):
    model = EventDate
    fields = [
        'date',
        'event',
    ]
    title = 'Datum hinzufügen'

    @property
    def success_url(self):
        return reverse_lazy(
            'vaple_core:index',
        )


class EventDateUpdate(generic.edit.UpdateView):
    model = EventDate
    fields = [
        'date',
    ]
    title = 'Datum bearbeiten'

    @property
    def success_url(self):
        return reverse_lazy(
            'vaple_core:index',
        )


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


class EventDateDelete(generic.edit.DeleteView):
    model = EventDate
    template_name_suffix = '_form'

    @property
    def success_url(self):
        return reverse_lazy(
            'vaple_core:index',
        )
