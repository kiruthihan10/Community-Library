from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Reader

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class ReaderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reader
        fields = ('address','user_name')