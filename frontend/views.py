from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse,HttpRequest
from .forms import EntryForm, SessionForm
from django.core import serializers
import requests

# Create your views here.

#when setClipboard is  called here the QueryDict is included in getClipboard
def index(request):
	form = EntryForm()
	form1 = SessionForm()
	

	if request.method == 'POST':
		form = EntryForm(request.POST)
		

		if len(form.data) != 0:
			# make call to setClipboard
			r = requests.post("http://localhost:8000/api/clipboard/",data = { 'data' :form.data['entry_data']})
			
			json = r.json()

			return redirect('results', data = json['id'])
			
	elif request.method == 'GET':
		form1 = SessionForm(request.GET)

		if len(form1.data) !=0 :

			#make call to getClipboard
			r = requests.get("http://localhost:8000/api/clipboard/" + form1.data['session_data'])
			json = r.json()
			return redirect('results', data = json['data'])
		else:
			form = EntryForm()
			form1 = SessionForm()
			return render(request,'frontend/index.html',{'form':form,'form1':form1})


def results(request, data):
	return render(request, 'frontend/results.html', {'token':data})

