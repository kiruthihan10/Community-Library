from rest_framework import serializers

from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name','author','price','language','quality','library_name']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['book_name','reader_name','date_added','ID']