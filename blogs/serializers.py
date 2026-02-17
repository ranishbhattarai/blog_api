from rest_framework import serializers
from .models import Blog
# this file is for serializing the Blog model, which allows us to convert Blog instances to and from JSON format when working with the API. It defines which fields of the Blog model should be included in the serialized output and which fields are read-only.
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published']
        read_only_fields = ['author', 'created_at', 'updated_at']