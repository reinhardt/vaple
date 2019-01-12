from django.urls import path
from . import views


app_name = 'vaple_core'
urlpatterns = [
    path('', views.EventOverview.as_view(), name='index'),
    path('events/add', views.EventCreate.as_view(), name='add_event'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='update_event'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='delete_event'),
    path('events/<int:pk>/dates/', views.EventDateList.as_view(), name='event_dates'),
    path('events/<int:pk>/dates/add', views.EventDateCreate.as_view(), name='add_event_date'),
    path('dates/add', views.EventDateCreate.as_view(), name='add_event_date'),
    path('dates/<int:pk>/update/', views.EventDateUpdate.as_view(), name='update_event_date'),
    path('dates/<int:pk>/delete/', views.EventDateDelete.as_view(), name='delete_event_date'),
]
