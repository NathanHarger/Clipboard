from rest_framework import serializers
from clipboard.models import Entry, FileEntry,TextEntry



class EntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Entry
		fields = ("session_id","creation_time",'media_type')


class FileEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = FileEntry
		fields = ("file", "entry_id")

class TextEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = TextEntry
		fields = ("text","entry_id")


