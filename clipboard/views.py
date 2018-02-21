from django.shortcuts import get_object_or_404, render,redirect

from django.http import HttpResponse,JsonResponse, Http404,FileResponse
from .models import Entry,TextEntry,FileEntry,MediaType
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from clipboard.serializers import EntrySerializer, TextEntrySerializer, FileEntrySerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import os 
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
        print("1.----------->")

        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.text)

    #create new entry and return the id 
    def post(self, request, format=None):

        media_type = request.data['media_type']
        #The creation of Objects is incorrect
        mt = MediaType(media_type_field=media_type)

        mt.save()

        entry = Entry(media_id=mt)
        entry.save()
        s = None

        #TODO Numbers being represented as strings
        if media_type == '0':

            s = TextEntry(text=request.data["text"],entry_id = entry)

        else:

            print("WTF?", type(request.data['file']))
            s = FileEntry(file=request.data["file"],entry_id = entry)

        s.save()

        return JsonResponse({'id':entry.session_id}, status=status.HTTP_201_CREATED)





#TODO Numbers represented as strings
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
        media_type = snippet.media_id
        media = None
        print("HERE", media_type.media_type_field)
        if media_type.media_type_field == '0':
            #get text
            media = TextEntry.objects.get(entry_id = session_id)
            serializer = TextEntrySerializer(media)
            return JsonResponse({'data':serializer.data['text']})

        
        elif media_type.media_type_field =='1':
            #get file
            media = FileEntry.objects.get(entry_id = session_id)
            serializer = FileEntrySerializer(media)
            fileLocation = serializer.data['file']

            return FileResponse(open(settings.BASE_DIR + fileLocation,'rb'))


   

class TextEntryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, session_id):
        try:
            return TextEntry.objects.get(entry_id=session_id)
        except TextEntry.DoesNotExist:
            raise Http404

    def get(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        serializer = TextEntrySerializer(snippet)
        return JsonResponse({'text':serializer.data['text']})

    

class FileEntryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, session_id):
        try:
            return FileEntry.objects.get(entry_id=session_id)
        except FileEntry.DoesNotExist:
            raise Http404

    def get(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        serializer = FileE(snippet)
        return JsonResponse({'file':serializer.data['file']})

    
