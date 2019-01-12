from datetime import date
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Event
from .models import EventDate


EVENT_FIELDS = [
            'title',
            'room',
            'sound_type',
        ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = EVENT_FIELDS

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
    model = Event
    template_name = 'vaple_core/event_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model._default_manager.all()
        return [(event, EventForm(instance=event)) for event in queryset]


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
            'vaple_core:event_dates',
            args=[self.object.event.id],
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
            'vaple_core:event_dates',
            args=[self.object.event.id],
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
            'vaple_core:event_dates',
            args=[self.object.event.id],
        )
