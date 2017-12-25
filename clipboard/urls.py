from django.urls import path

from . import views

urlpatterns = [
	
	path('getClipboard/<str:token>',views.getClipboard,name="getClipboard"),
	path('setClipboard/<str:data>',views.setClipboard,name="setClipboard"),

]