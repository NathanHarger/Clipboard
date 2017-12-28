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
		form1 = SessionForm(request.POST)
		if len(form1.data) != 0:
			# make call to setClipboard
			print(form1.data)
			r = requests.post("http://localhost:8000/api/clipboard/",data = { 'data' :form1.data['data']})
			print(r.json())
			json = r.json()
			print(json['id'])

			return redirect('results', data = json['id'])
			
	elif request.method == 'GET':
		form = EntryForm(request.GET)
		print(form.data)

		if len(form.data) !=0 :
			print(form.data)

			#make call to getClipboard
			r = requests.get("http://localhost:8000/api/clipboard/" + form.data['data'])
			json = r.json()
			print(json)
			return redirect('results', data = json['data'])
		else:
			form = EntryForm()
			form1 = SessionForm()
			return render(request,'frontend/index.html',{'form':form,'form1':form1})


def results(request, data):
	return render(request, 'frontend/results.html', {'token':data})

