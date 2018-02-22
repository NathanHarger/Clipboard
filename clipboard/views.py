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
import urllib.parse
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



import mimetypes
import re
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
            file_name = re.search(r'[a-zA-z0-9 ]+\.[a-zA-Z0-9]+', fileLocation).group()
            file_path = settings.BASE_DIR + fileLocation
            print("file_name", file_name)
            print("file_path", file_path)
            return respond_as_attachment(request, file_path, file_name)

def respond_as_attachment(request, file_path, original_filename):
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    response['X-Sendfile'] = file_path
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

    
