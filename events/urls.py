#  -- events/urls.py
from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('events/', events, name='events'),
    path('events/create', event_view, name='event_create'), # Create mode
    path('event/<slug:slug>/admin/<slug:admin_code>', event_view, name='event_admin'), # Edit Mode (Admin)
    path('event/<slug:slug>/register', event_view, name='event_register'), # Registration Mode (Public)
    path('event/<slug:slug>/delete/', delete_event, name='delete_event'),    

    path('add_participant/', participation, name='add_participant'),
    path('edit_participant/<slug:slug>', participation, name='edit_participant'),
    path('delete_participant/<slug:slug>', delete_participation, name='delete_participant'),
    
    path('event/<slug:slug>/participant/<slug:participant_code>', participant_view, name='participant_view'), # Edit Mode (Adm
]
