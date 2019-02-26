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
    path('export-full', views.EventOverviewExport.as_view(), name='export-full'),
    path('export-employee/<int:pk>', views.EmployeeExport.as_view(), name='export-employee'),
    path('export-employees-batch', views.batch_employee_export, name='export-employees-batch'),
    path('events/<int:pk>/folder', views.event_folder, name='event_folder'),
    path('events/<int:pk>/folder_open', views.event_folder_open, name='event_folder_open'),
]
