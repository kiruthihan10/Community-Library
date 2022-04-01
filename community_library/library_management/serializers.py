from rest_framework import serializers

from .models import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['name','address','subscription_fee','librarian_name']

class LibraryParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['name','address','subscription_fee']

class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['user_name','library_name','banned','fine']