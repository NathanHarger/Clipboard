
import urllib.parse
import os 
import mimetypes
import re
import json

from .models import Entry,TextEntry,FileEntry,MediaType, FileMetaEntry
from clipboard.serializers import EntrySerializer, TextEntrySerializer, FileEntrySerializer,FileMetaEntrySerializer

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


class EntryMetaDataDetail(APIView):
    def get_object(self, session_id):
        try:
            return Entry.objects.get(session_id=session_id)
        except Entry.DoesNotExist:
            raise Http404
    def get(self, request,session_id=None, format=None):
        print("running get meta data")
        if(session_id == None):
            session_id = request.GET.get('session_id')
        entry = self.get_object(session_id)

        
        entry_serializer = EntrySerializer(entry)
        print("WERFSDAF", entry.media_id)
        media = entry.media_id
        media_type = int(media.media_type_field)
        if media_type == 1:
            fmd = FileMetaEntry.objects.get(file_entry_id =entry)
            fmds = FileMetaEntrySerializer(fmd)
            return JsonResponse({"entry" :entry_serializer.data ,"media_type":media.media_types[media_type][1], "FileMetaData":fmds.data}) 
        else:
            return JsonResponse({"entry" :entry_serializer.data ,"media_type":media.media_types[media_type][1]}) 


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
            s.save()

        else:

            s = FileEntry(file= request.data["file"],entry_id = entry)
            s.save()
            print("_______?", s.file)
            type, encoding = mimetypes.guess_type(s.file.name)
            size = len(request.data[s.file.name])

            fme = FileMetaEntry(file_entry_id = entry, file_name = s.file,file_type=type, file_length= size)
            fme.save()

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
        entry = self.get_object(session_id=session_id)
        media_type = entry.media_id
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
            file_metadata = FileMetaEntry.objects.get(file_entry_id = entry)

            print("WTF", media.file)
            serializer = FileEntrySerializer(media)
            fileLocation = serializer.data['file']

            file_name = file_metadata.file_name
            file_path = settings.BASE_DIR + fileLocation
            self.delete(request,session_id)

            return respond_as_attachment(request, file_path, file_name, file_metadata.file_type)
    
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



def respond_as_attachment(request, file_path, original_filename, file_format):
    
    def generate():
        with open(file_path, 'rb') as f:
            yield from f

        os.remove(file_path)

    #fp = open(file_path, 'rb')
    response = HttpResponse(generate())
    if file_format is None:
        file_format = 'application/octet-stream'
    response['Content-Type'] = file_format
    if file_format is not None:
        response['Content-Encoding'] = file_format

    
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

    
