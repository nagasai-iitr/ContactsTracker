from django.urls import path
from .views import identify_view

urlpatterns = [
    path('identify/', identify_view, name='identify'),
]