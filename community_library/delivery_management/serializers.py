from rest_framework import serializers

from .models import *

class BorrowelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowel
        fields = ['reader_name', 'book_name', 'start_date', 'return_date', 'deadline', 'start_quality', 'end_date']

class BorrowelDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['reader_name','book_name','deadline']

class ExtendSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowelExtend
        fields = ['user_name','book_name']
