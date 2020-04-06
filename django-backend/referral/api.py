from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse
from referral.models import Page, Referrer
from django.db import models

# test message for API activity
@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def getTest(request):
    return JsonResponse({'message': 'API is live'}, safe=True)

# endpoint for data on the single seed page
@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def getPage(request):
    # Rather than setting up token auth flow, simply grab the seeded data from `fixtures/seeds.json`
    pages = Page.objects.filter(pk='1').values('name', 'owner')
    referrers = Referrer.objects.filter(page_id='1').values('name', 'count', 'created_at', 'last_modified')
    # convert queryset to python list to parse for JsonResponse
    pages_list = list(pages)
    referrers_list = list(referrers)
    # store data in a dictionary for JsonResponse
    page_data = {
        'page': pages_list[0],
        'referrers': referrers_list
    }

    return JsonResponse(page_data, safe=True)