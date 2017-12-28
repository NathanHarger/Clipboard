from django.urls import path

from . import views

urlpatterns = [
	
	path('index/',views.index,name="index"),
	path('results/<str:data>/',views.results,name="results"),

]