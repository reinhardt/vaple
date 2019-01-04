from django.shortcuts import render
from .models import Event


def index(request):
    events = Event.objects.order_by('-title')[:50]
    context = {
        'events': events,
    }
    return render(request, 'vaple_core/index.html', context)


def add_event(request):
    context = {
    }
    return render(request, 'vaple_core/add_event.html', context)
