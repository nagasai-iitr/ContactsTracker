from django.shortcuts import render
from django.http import JsonResponse
from .models import Contact
import json
# Create your views here.

def identify_view(request):
    data = json.loads(request.body)
    if 'email' in data:
        email = data['email']
    if 'phoneNumber' in data:
        phoneNumber = data['phoneNumber']
    
    return JsonResponse(data)