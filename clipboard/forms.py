from django import forms
from clipboard.models import Entry


class EntryForm(forms.Form):
	data = forms.CharField(label="Enter Data", required=True, max_length=1000)
