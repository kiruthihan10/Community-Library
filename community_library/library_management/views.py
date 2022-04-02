from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Library, MemberShip
from .serializers import *

from user_management.models import Librarian, Reader
from user_management.validate_and_extract import *
from user_management.serializers import ReaderSerializer

from book_management.models import Book
from book_management.serializers import BookSerializer
from book_management.validate_and_extract import *


def library_view_post(request):
    if not request.user.is_superuser:
        return UNAUTH_RESPONSE
    data = request.data.copy()
    reader = extract_reader(user_name = data['librarian'])
    if type(reader) == Reader:
        serializer =  LibraryParameterSerializer(data=data)
        if serializer.is_valid():
            librarian = Librarian(reader=reader)
            librarian.save()
            library = Library(
                name = data['name'],
                address = data['address'],
                subscription_fee = data['subscription_fee'],
                librarian = librarian
            )
            library.save()
            return Response(self.serializer_class(instance=library).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return reader

@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsAuthenticated, ))
def library_view(request):
    if request.method == 'GET':
        libraries = Library.objects.all()
        serializer = LibrarySerializer(instance = library)
        return JsonResponse(serializer.data, status= status.HTTP_200_OK)
    elif request.method == 'POST':
        return library_view_post(request)
    elif request.method == 'PUT':
        librarian = extract_librarian(request.user)
        try:
            library = Library.objects.get(librarian = librarian)
        except:
            return HttpResponse("Librarian Does Not have Library", status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        return specific_library_put(request, library.ID)
    else:
        return BAD_REQUEST_METHOD_RESPONSE
        
def specific_library_get(library_id):
    library = extract_library(library_id)
    if type(library) == Library:
        serializer = LibrarySerializer(instance = library)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    return library

def specific_library_put(request, library_id):
    library = extract_library(library_id)
    if type(library) == Library:
        data = request.data
        if library.librarian.reader.user_name() != data['librarian']:
            new_librarian = True
            old_librarian = library.librarian
            reader = extract_reader(user_name = data['librarian'])
            if type(reader) == Reader:
                librarian = Librarian(reader = reader)
                librarian.save()
            return reader
        else:
            new_librarian = False
            librarian = library.librarian
        library.name = data['name']
        library.subscription_fee = data['subscription_fee']
        library.address = data['address']
        library.librarian = librarian
        library.save()
        if new_librarian:
            old_librarian.delete()
        serializer = LibrarySerializer(instance = library)
        return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
    return library

def specific_library(request, library_id):
    if request.method == 'GET':
        specific_library_get
    elif request.method == 'PUT':
        specific_library_put(request, library_id)
    return BAD_REQUEST_METHOD_RESPONSE

def specific_library_librarian(request, library_id):
    library = validate_and_extract_library(request, library_id)
    if type(library) == Library:
        serializer = ReaderSerializer(instance = library.librarian)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    return library

def specific_library_inventory(request, library_id):
    library = validate_and_extract_library(request, library_id)
    if type(library) == Library:
        books = Book.objects.filter(library=library)
        return serialize_book(book)
    return library

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def specific_library_ban_user(library, user_name):
    if request.method != 'POST':
        return BAD_REQUEST_METHOD_RESPONSE
    user = request.user
    librarian = extract_librarian(user)
    library = derive_library_from_librarian(librarian)
    if type(library) == Library:
        if library.ID == library_id:
            reader = extract_reader(user_name)
            if type(reader) == Reader:
                membership = extract_membership(library, reader)
                if type(membership) == MemberShip:
                    membership.ban()
                    serializer = MemberShipSerializer(instance = membership)
                    return JsonResponse(serializer.data, status= status.HTTP_200_OK)
                return membership
            return reader
        return UNAUTHORIZED_ACCESS_RESPONSE
    return library



# Create your views here.
