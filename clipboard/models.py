from django.db import models
import random
import string

# Create your models here.

def get_default_id():
	return ''.join([random.choice(string.ascii_letters+string.digits) for ch in range(8)])
class MediaType(models.Model):
	media_types = ((0, 'Text'),(1, 'File'),)	
	media_type_field = models.CharField(max_length=1, choices=media_types)



class Entry(models.Model):

	session_id =  models.CharField(max_length=8,default=get_default_id, primary_key=True)
	creation_time = models.DateTimeField(auto_now = True)
	media_id = models.ForeignKey(MediaType, on_delete=models.CASCADE)



class FileEntry(models.Model):
	file = models.FileField()
	entry_id = models.OneToOneField(Entry,on_delete=models.CASCADE,    primary_key=True    )


class TextEntry(models.Model):
	text = models.CharField(max_length = 1000)
	entry_id = models.OneToOneField(Entry,on_delete=models.CASCADE,    primary_key=True    )


