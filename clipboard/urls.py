from django.urls import path

from . import views

urlpatterns = [

	path('', views.index, name='index'),
	path('results/<int:entry_id>',  views.results, name="results"),
]