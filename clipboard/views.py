from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import EntryForm
from .models import Entry
from django.core import serializers

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
	entry = get_object_or_404(Entry, session_id=token)
	json = {"id":entry.session_id, "data":entry.data}
	return JsonResponse(json)

def setClipboard(request, data):
	newEntry = Entry(data = data)
	newEntry.save()
	json = {"id" : newEntry.session_id}
	return JsonResponse(json)
