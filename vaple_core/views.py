from datetime import date
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Event
from .models import EventDate


def index(request):
    events = Event.objects.order_by('-title')[:50]
    context = {
        'events': events,
    }
    return render(request, 'vaple_core/index.html', context)


class EventCreate(generic.edit.CreateView):
    model = Event
    fields = [
        'title',
        'room',
    ]
    success_url = reverse_lazy('vaple_core:index')
    title = 'Veranstaltung hinzufügen'


class EventUpdate(generic.edit.UpdateView):
    model = Event
    fields = [
        'title',
        'room',
    ]
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
