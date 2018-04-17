from rest_framework import serializers
from clipboard.models import Entry, FileEntry,TextEntry, MediaType, FileMetaEntry
from django.contrib.auth.models import User


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

class SignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields=('username', 'password')
		write_only_fields = ('password',)

	