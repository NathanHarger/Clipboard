from django.shortcuts import get_object_or_404, render,redirect

from django.http import HttpResponse,JsonResponse, Http404
from .models import Entry
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from clipboard.serializers import EntrySerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status


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

class EntryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("ran")
        d = Entry.objects.create(data=request.data["data"])

        return JsonResponse({'id':d.session_id}, status=status.HTTP_201_CREATED)



class EntryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, session_id):
        try:
            return Entry.objects.get(session_id=session_id)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        serializer = EntrySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        serializer = EntrySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
