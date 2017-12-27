from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Entry
from django.core import serializers
import json

# Create your views here.


# def index(request):
# 	if request.method == 'POST':
# 		form = EntryForm(request.POST)
# 		if form.is_valid():
# 			newEntry = Entry(data = form.data)
# 			newEntry.save()
# 			return redirect('results', entry_id =newEntry.id)

# 	else:
# 		form = EntryForm()
# 		return render(request,'clipboard/index.html',{'form':form})


# def results(request, entry_id):
# 	entry = get_object_or_404(Entry,pk=entry_id)
# 	return render(request, 'clipboard/results.html', {'token':entry.session_id})

def getClipboard(request, token):
	entry = get_object_or_404(Entry.objects, session_id=token)
	d = {'id':entry.session_id, 'data':entry.data}
	return JsonResponse(d)

def setClipboard(request, data):
	
	newEntry = Entry.objects.create(data = data)
	newEntry.save()
	d = {'id' : newEntry.session_id}
	return JsonResponse(d)
