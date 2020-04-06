from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json
from django.http import JsonResponse
from referral.models import Page, Referrer
from django.db import models

# endpoint for testing server status
@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def getTest(request):
    return JsonResponse({'message': 'API is live'}, safe=True, status=200)

# endpoint for getting data on the single seed page's referrals
# TODO: refactor to pull page id based on request token header
@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def getPage(request):
    # grab the seeded data from `fixtures/seeds.json`
    pages = Page.objects.filter(pk='1').values('name', 'owner')
    referrers = Referrer.objects.filter(page_id='1').values('name', 'link', 'count', 'created_at', 'last_modified')
    # convert queryset to python list to parse for JsonResponse
    pages_list = list(pages)
    referrers_list = list(referrers)
    # store data in a dictionary for JsonResponse
    page_data = {
        'page': pages_list[0],
        'referrers': referrers_list
    }

    return JsonResponse(page_data, safe=True, status=200)

# endpoint for crediting referrer for a pageview
# client will send a POST request with JSON body {page_id: id, referrer: name}
# TODO: refactor to verify page id based on request token header
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def creditReferrer(request):
    data = json.loads(request.body)
    # pull out page_id and link for readability
    page_id = data['page_id']
    link = data['link']
    # determine if link and page_id are valid, else return 500 error
    try:
        referrer = Referrer.objects.get(page_id=page_id, link=link)
        referrer.count += 1
        referrer.save()
        return JsonResponse({"message": "Referrer given credit for pageview"}, safe=True, status=200)
    except Referrer.DoesNotExist:
        return JsonResponse({"message": "ERROR: hat referrer link was not valid"}, safe=True, status=500)