from django.urls import path
from .views import planner_view, add_event, edit_event, delete_event

app_name = 'planner'

urlpatterns = [
    path('', planner_view, name='planner_view'),
    path('add/', add_event, name='add_event'),
    path('edit/<int:event_id>/', edit_event, name='edit_event'),
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
    # path('events/', views.get_events, name='get_events'),  
]