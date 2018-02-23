from django.urls import path


from . import views
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
	
	path('', TemplateView.as_view(template_name="index.html")),


]