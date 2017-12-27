from django import forms
from clipboard.models import Entry


class EntryForm(forms.Form):
	data = forms.CharField(label="Enter Data", required=False, max_length=1000)
	
class SessionForm(forms.Form):
    data = forms.CharField(label="Enter Id", required = False, max_length=8)

