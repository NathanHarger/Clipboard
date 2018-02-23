from django.urls import path

from . import views
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
	
	path('index/',views.index,name="index"),
	url(r'^', TemplateView.as_view(template_name="index.html")),


]