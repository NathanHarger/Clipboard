
import urllib.parse
import os 
import mimetypes
import re
import json
import boto3
import requests
from .models import Entry,TextEntry,FileEntry,MediaType, FileMetaEntry
from clipboard.serializers import EntrySerializer, TextEntrySerializer, FileEntrySerializer,FileMetaEntrySerializer, SignUpSerializer

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse, Http404,FileResponse
from django.core import serializers
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from oauth2_provider.models import Application
from oauth2_provider.views.generic import ProtectedResourceView

#from rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication,TokenHasScope
from django.views.decorators.csrf import ensure_csrf_cookie

class EntryMetaDataDetail(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    

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
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    

    def get(self, request):
       return HttpResponse("no get")
    
    #create new entry and return the id 

    def post(self, request, format=None):

        print(request.data)
        if "text" in request.data:
            media_type = 0
        elif "file" in request.data:
            media_type = 1
        else:
            return JsonResponse({'error_message':"missing file or text field"}, status=status.HTTP_400_BAD_REQUEST)

        #The creation of Objects is incorrect
        mt = MediaType(media_type_field=media_type)

        mt.save()
     

        entry = Entry(media_id=mt, user = request.user.get_username())

        entry.save()
        print("media_type", media_type)
        if media_type == 0:
            text = request.data["text"]
            size = len(text)

            if(size > 1000):
                return JsonResponse({'error_message':'1000 character limit'}, status=status.HTTP_409_CONFLICT)
    
            s = TextEntry(text=request.data["text"],entry_id = entry)
            s.save()

        else:
            file = request.data['file']
            print(file)
            size = len(file)
            print(size)

            if(size >= 1000024):
                return JsonResponse({'error_message':'File too large, 1MB limit'}, status=status.HTTP_409_CONFLICT)
    
            type, encoding = mimetypes.guess_type(request.data['file'].name)

            len(file)
            s = FileEntry(file= request.data["file"],entry_id = entry)
            s.save()
            print("_______?", s.file)
            

            fme = FileMetaEntry(file_entry_id = entry, file_name = s.file,file_type=type, file_length= size)
            fme.save()

        return JsonResponse({'id':entry.session_id}, status=status.HTTP_201_CREATED)


#TODO Numbers represented as strings
class EntryDetail(APIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    
    """
    Retrieve, update or delete a snippet instance.
    """
   

    def get_object(self, session_id):
        try:
            return Entry.objects.get(session_id=session_id)
        except Entry.DoesNotExist:
            return None
    def get(self, request, session_id=None, format=None):
        print("called")
        if(session_id == None):
            session_id = request.GET.get('session_id')
        print(session_id)
        entry = self.get_object(session_id=session_id)
        user = request.user.get_username()
        if entry == None or entry.user != user:
            return JsonResponse({"error_message":"Invalid session-id"}, status=status.HTTP_409_CONFLICT)

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

            serializer = FileEntrySerializer(media)
            fileLocation = serializer.data['file']

            file_name = file_metadata.file_name
            if not settings.DEBUG:
                file_path = settings.AWS_S3_CUSTOM_DOMAIN + fileLocation
            else:
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
    
    if not settings.DEBUG:
        s3 = boto3.resource('s3')
        obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME,'media/'+original_filename)
        data = obj.get()['Body'].read(amt=1024)
        response = HttpResponse(data)
    else:
        def generate():
            with open(file_path, 'rb') as f:
                yield from f

            os.remove(file_path)
        response = HttpResponse(generate())

    #fp = open(file_path, 'rb')
    if file_format is None:
        file_format = 'application/octet-stream'
    response['Content-Type'] = file_format
    if file_format is not None:
        response['Content-Encoding'] = file_format

    
    filename_header = 'filename=' + original_filename
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response

class TextEntryDetail(APIView):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    
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

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    

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

class SignUp(APIView):
    permission_classes = [AllowAny]
    
    #def get(self,request):
     #   return JsonResponse({'error_message': "Must be POST"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):

        
        if 'username' not in request.data or 'password' not in request.data:
            return JsonResponse({'error_message':'Require username and password as form data'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.data['username']
        if len(user) > 10:
            return JsonResponse({'error_message': user + " is over 10 characters"}, status=status.HTTP_401_UNAUTHORIZED)

        print(user)
        try:
            userobj = User.objects.all().get(username=user)
        except:
            userobj = None
        if(userobj == None):
            User.objects.create_user(username=user,  password=request.data['password'])
            r = requests.post(settings.URL_HOST + "o/token/", data ={"username":user, "password":request.data['password'], 
                                                                        "grant_type":"password", 
                                                                        "client_id":"Wdj99Y5tK42ibtrCqhnxyd4Cy4E9i2HQiV0kmUVP"})
            django_response = HttpResponse(
            content=r.content,
            status=r.status_code,
            content_type=r.headers['Content-Type'],

            )
            return django_response
        return JsonResponse({'error_message': user + " is already taken"}, status=status.HTTP_401_UNAUTHORIZED)

