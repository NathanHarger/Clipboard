from django.db import models
import random
import string

# Create your models here.

def get_default_id():
	return ''.join([random.choice(string.ascii_letters+string.digits) for ch in range(8)])

class Entry(models.Model):

	session_id =  models.CharField(max_length=8,default=get_default_id)
	data = models.CharField(max_length = 1000)
	
	def __str__(self):
		return self.session_id + " " + self.data



	 