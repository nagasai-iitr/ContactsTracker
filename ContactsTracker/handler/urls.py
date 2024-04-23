from django.urls import path
from .views import identify_view, get_contacts_view

urlpatterns = [
    path('identify', identify_view, name='identify'),
    path('contacts', get_contacts_view, name='contacts'),
]