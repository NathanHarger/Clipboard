from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse,HttpRequest
from .forms import FileEntryForm,TextEntryForm,EntryForm
from django.core import serializers
import requests

# Create your views here.

#when setClipboard is  called here the QueryDict is included in getClipboard
def index(request):
	session_id_form = EntryForm()
	form = TextEntryForm()
	form1 = FileEntryForm()
	
	#TODO write validation for forms instead of len(form.data) !=0
	if request.method == 'POST':
		form = TextEntryForm(request.POST)
		form1 = FileEntryForm(request.POST, request.FILES)
		print("form", form.data)
		print("form1", form1.data)
		if  "text" in form.data:
			# make call to setClipboard

			r = requests.post("http://localhost:8000/api/clipboard/",data = { 'text' :form.data['text'], 'media_type':0})

			json = r.json()

			return redirect('results', data = json['id'])
		elif "file" in form1.data:
			print("test")
			#form1.save()
			r = requests.post("http://localhost:8000/api/clipboard/",data = { 'file' :form1.data['file'], 'media_type':1})
			json = r.json()
			return redirect('results', data = json['id'])
	elif request.method == 'GET':
		session_id_form = EntryForm(request.GET)

		if len(session_id_form.data) !=0 :

			#make call to getClipboard
			r = requests.get("http://localhost:8000/api/clipboard/" + session_id_form.data['session_id'])
			json = r.json()
			print("WTF", json)
			return redirect('results', data = json['data'])
		else:
			form = TextEntryForm()
			form1 = FileEntryForm()
			session_id_form = EntryForm()
			return render(request,'frontend/index.html',{'form':form,'form1':form1, 'session_id_form': session_id_form})


def results(request, data):
	return render(request, 'frontend/results.html', {'token':data})

