from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json

@csrf_exempt
def identify_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')
        
        if not email and not phoneNumber:
            return JsonResponse({'message': "incomplete data"})
        
        # get the primary contacts for our request
        query = Q()
        # handle the cases with None input
        if email:
            query |= Q(email = email)
        if phoneNumber:
            query |= Q(phoneNumber = phoneNumber)
            
        primary_contacts = Contact.objects.filter(query, linkPrecedence='primary').order_by('createdAt')#.values()
        
        # case 1, if there is no new information
        if Contact.objects.filter(Q(email=email) & Q(phoneNumber=phoneNumber)).exists():
            primary_id = Contact.objects.filter(Q(email=email) & Q(phoneNumber=phoneNumber)).first().linkedId or Contact.objects.filter(Q(email=email) & Q(phoneNumber=phoneNumber)).first().id
        # case 2, there are no primary contacts
        elif not primary_contacts.exists():
            new_contact = Contact.objects.create(
                email = email,
                phoneNumber = phoneNumber,
            )
            primary_id = new_contact.id
        # case 3, there is only one primary contact
        elif primary_contacts.count() == 1:
            # case 3.a if email exists and thats not the common element
            if email and email != primary_contacts.first().email:
                new_contact = Contact.objects.create(
                    email = email,
                    phoneNumber = primary_contacts.first().phoneNumber,
                    linkedId = primary_contacts.first().id,
                    linkPrecedence = 'secondary',
                )
            # case 3.b if phoneNumber exists and thats not the common element
            if phoneNumber and phoneNumber != primary_contacts.first().phoneNumber:
                new_contact = Contact.objects.create(
                    email = primary_contacts.first().email,
                    phoneNumber = phoneNumber,
                    linkedId = primary_contacts.first().id,
                    linkPrecedence = 'secondary',
                )
            primary_id = primary_contacts.first().id
        # case 4, there are more than one primary contacts
        else:
            primary_id = primary_contacts.first().id
            temp_contact = primary_contacts[1]
            secondary_contacts = Contact.objects.filter(linkPrecedence = 'secondary', linkedId = temp_contact.id)#.values()
            # update the contacts which are linked to the new primary contact
            for contact in secondary_contacts:
                contact.linkedId = primary_id
                contact.save()
            # update the newer primary contact linking to oldest primary contact
            temp_contact.temp_contact = 'secondary'
            temp_contact.linkedId = primary_id
            temp_contact.save()
        
        # now that we have the primary contact id we need to fetch corresponding secondary contacts linked to it
        secondary_contacts = Contact.objects.filter(linkedId=primary_id)#.values()
        primary_contact = Contact.objects.get(id=primary_id)
        # generate the JSON response
        response_data = {
            "contact": {
                "primaryContactId": primary_contact.id,
                "emails": [primary_contact.email] if primary_contact.email is not None else [],
                "phoneNumbers": [primary_contact.phoneNumber],
                "secondaryContactIds": []
            }
        }
        for contact in secondary_contacts:
            if contact.email is not None and contact.email not in response_data["contact"]["emails"]:
                response_data["contact"]["emails"].append(contact.email)
            if contact.phoneNumber is not None and contact.phoneNumber not in response_data["contact"]["phoneNumbers"]:
                response_data["contact"]["phoneNumbers"].append(contact.phoneNumber)
            response_data["contact"]["secondaryContactIds"].append(contact.id)
            
        return JsonResponse(response_data)

def get_contacts_view(request):
    '''
    A view function to return all the data just for testing puspose
    '''
    contacts = Contact.objects.all()#.values_list('id', 'phoneNumber', 'email', 'linkedId', 'linkPrecedence')
    out = {"contacts":[]}
    for contact in contacts:
        out["contacts"].append({"id":contact.id, "phoneNumber":contact.phoneNumber, "email":contact.email, "linkedId":contact.linkedId, "linkPrecedence":contact.linkPrecedence})
    
    return JsonResponse(out) 