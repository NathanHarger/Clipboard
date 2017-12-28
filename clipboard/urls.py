from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	
   
 url(r'^clipboard/$', views.EntryList.as_view()),
    url(r'^clipboard/(?P<session_id>[a-zA-Z0-9]+)/$', views.EntryDetail.as_view()),

]


