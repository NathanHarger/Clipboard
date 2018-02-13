from rest_framework import serializers
from clipboard.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("data", "session_id","creation_time")
    