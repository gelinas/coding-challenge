from django.conf.urls import url
from . import api

urlpatterns = [
    url('test', api.getTest),
    url('page', api.getPage),
]