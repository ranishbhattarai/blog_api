from rest_framework import serializers
from .models import CustomUser
# this file is for serializing the CustomUser model, which is used in the Blog model as a foreign key. It allows us to convert CustomUser instances to and from JSON format when working with the API.
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role',]

