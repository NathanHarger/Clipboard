
import urllib.parse
import os 
import mimetypes
import re
import json

from .models import Entry,TextEntry,FileEntry,MediaType
from clipboard.serializers import EntrySerializer, TextEntrySerializer, FileEntrySerializer

from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse, Http404,FileResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status



class EntryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.text)

    #create new entry and return the id 
    def post(self, request, format=None):
        print("WTF" ,request.data)
        if "text" in request.data:
            media_type = 0
        else:
            media_type = 1

        #The creation of Objects is incorrect
        mt = MediaType(media_type_field=media_type)

        mt.save()

        entry = Entry(media_id=mt)
        entry.save()
        s = None
        print("media_type", media_type)
        if media_type == 0:

            s = TextEntry(text=request.data["text"],entry_id = entry)

        else:

            s = FileEntry(file= request.data["file"],entry_id = entry)

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


    def get(self, request, session_id=None, format=None):
        if(session_id == None):
            session_id = request.GET.get('session_id')
        print(session_id)
        snippet = self.get_object(session_id=session_id)
        media_type = snippet.media_id
        media = None
        if media_type.media_type_field == '0':
            #get text
            media = TextEntry.objects.get(entry_id = session_id)
            serializer = TextEntrySerializer(media)
            self.delete(request,session_id)
            return JsonResponse({'data':serializer.data['text']})

        
        elif media_type.media_type_field == '1':
            #get file
            media = FileEntry.objects.get(entry_id = session_id)
            serializer = FileEntrySerializer(media)
            fileLocation = serializer.data['file']

            print("Test", fileLocation)
            file_name = re.search(r'[a-zA-z0-9 ]+\.[a-zA-Z0-9]+', fileLocation).group()
            file_path = settings.BASE_DIR + fileLocation
            self.delete(request,session_id)

            return respond_as_attachment(request, file_path, file_name)
    
    #TODO Numbers represented as strings
    def delete(self, request, session_id, format=None):
        snippet = self.get_object(session_id=session_id)
        media_type = snippet.media_id
        if media_type.media_type_field == '1':
            file_entry = FileEntry.objects.get(entry_id = session_id)
            filename = file_entry.file
           

            # file can't be deleted since its required to be on disk to be
            # served to frontend
            #try:
                #os.remove(settings.BASE_DIR +'/uploads/' +str(filename))
           #except:
            #    print("invalid file")

        snippet.delete()



def respond_as_attachment(request, file_path, original_filename):
    
    def generate():
        with open(file_path, 'rb') as f:
            yield from f

        os.remove(file_path)

    #fp = open(file_path, 'rb')
    response = HttpResponse(generate())
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    if encoding is not None:
        response['Content-Encoding'] = encoding

    
    filename_header = 'filename=' + original_filename
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response

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

    
