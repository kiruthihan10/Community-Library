from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Reader
from library_management.models import MemberShip

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class ReaderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reader
        fields = ('address','user_name')

class ReaderRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reader
        fields = ('ratings','user_name')

class ReaderMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ('user_name','library_name','banned','fine','library_id')