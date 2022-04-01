from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status


from .models import Library, MemberShip
from .serializers import *

from user_management.models import Librarian, Reader
from user_management.validate_and_extract import *
from user_management.serializers import ReaderSerializer


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def create(self, request):
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
    
    def update(self, *args, **kwargs):
        return BAD_REQUEST_METHOD_RESPONSE

    def destroy(self, request):
        return BAD_REQUEST_METHOD_RESPONSE

    def partial_update(self, request):
        return BAD_REQUEST_METHOD_RESPONSE

def specific_library(request, library_id):
    if request.method == 'GET':
        library = extract_library(library_id)
        if type(library) == Library:
            serializer = LibrarySerializer(instance = library)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        return library
    elif request.method == 'PUT':
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
        pass

def specific_library_ban_user(request, library_id, user_name):
    library = validate_and_extract_library(request, library_id)
    if type(library) == Library:
        reader = extract_reader(request, user_name)
        if type(reader) == Reader:
            membership = extract_membership(library, reader)
            if type(membership) == MemberShip:
                membership.ban()
                serializer = MemberShipSerializer(instance = membership)
                return JsonResponse(serializer.data, status= status.HTTP_200_OK)
            return membership
        return reader
    return library


# Create your views here.
