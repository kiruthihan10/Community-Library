from rest_framework import serializers

from .models import *

class BorrowelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowel
        fields = ['reader_name', 'book_name', 'start_date', 'return_date', 'deadline', 'start_quality', 'end_date']

class BorrowelDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowel
        fields = ['reader_name','book_name','deadline']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['user_name','book_name','Date_applied','ID']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user_name','head','body']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = ['by_id','on_id','date','ID']