from django import forms
from clipboard.models import Entry, FileEntry,TextEntry

class EntryForm(forms.Form):
	session_id = forms.CharField(label="Enter Id", required = False, max_length=8)


class FileEntryForm(forms.ModelForm):
	class Meta:
		model = FileEntry
		fields = ("file", )

class TextEntryForm(forms.ModelForm):
	class Meta:
		model = TextEntry
		fields = ("text",)

	 
