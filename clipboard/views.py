from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from .forms import EntryForm
from .models import Entry
# Create your views here.

def index(request):
	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			newEntry = Entry(data = form.data)
			newEntry.save()
			return redirect('results', entry_id =newEntry.id)

	else:
		form = EntryForm()
		return render(request,'clipboard/index.html',{'form':form})


def results(request, entry_id):
	entry = get_object_or_404(Entry,pk=entry_id)
	return render(request, 'clipboard/results.html', {'token':entry.session_id})

