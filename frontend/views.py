from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import EntryForm, SessionForm
from django.core import serializers
import requests

# Create your views here.

#when setClipboard is  called here the QueryDict is included in getClipboard
def index(request):
	if request.method == 'POST':
			form = EntryForm(request.POST)
			form1 = SessionForm(request.POST)
			if form1.is_valid():
				# make call to setClipboard
				r = requests.get('http://localhost:8000/clipboard/setClipboard/'+form1.data["data"])
				json = r.json()
				return redirect('results', data = json["id"])
			else:
				#make call to getClipboard
				r = requests.get('http://localhost:8000/clipboard/getClipboard/'+ form.data["data"])
				json = r.json()
				return redirect('results', data = json["data"])

	else:
		form = EntryForm()
		form1 = SessionForm()
	return render(request,'frontend/index.html',{'form':form,'form1':form1})


def results(request, data):
	return render(request, 'frontend/results.html', {'token':data})

