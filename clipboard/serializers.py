from rest_framework import serializers
from clipboard.models import Entry, FileEntry,TextEntry, MediaType, FileMetaEntry



class EntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Entry
		fields = ("session_id","creation_time")


class FileEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = FileEntry
		fields = ("file", "entry_id")

class TextEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = TextEntry
		fields = ("text","entry_id")


class FileMetaEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = FileMetaEntry
		fields=("file_name", "file_length","file_type")

	