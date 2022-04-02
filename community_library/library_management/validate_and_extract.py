from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponse

from .models import Library, MemberShip

from user_management.validate_and_extract import *

from community_library.validate_and_extract import *

MEMBERSHIP_DOES_NOT_EXIST_RESPONSE = HttpResponse('Membership Does Not Exist', status=status.HTTP_204_NO_CONTENT)

LIBRARY_DOES_NOT_EXIST_RESPONSE = HttpResponse('Library Does Not Exist', status=status.HTTP_204_NO_CONTENT)

def extract_library(library_id):
    try:
        return Library.objects.get(pk=library_id)
    except User.DoesNotExist:
        return USER_DOES_NOT_EXIST_RESPONSE

def validate_and_extract_library(request, library_id):
    if request.method == 'GET':
        return extract_library(library_id)
    return BAD_REQUEST_METHOD_RESPONSE

def extract_membership(library, reader):
    try:
        return MemberShip.objects.get(lib=library,reader=reader)
    except MemberShip.DoesNotExist:
        return MEMBERSHIP_DOES_NOT_EXIST_RESPONSE

def derive_library_from_librarian(librarian):
    try:
        library = Library.objects.get(librarian = librarian)
    except Library.DoesNotExist:
        return HttpResponse("Librarian does not have a library", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return library

def derive_library_from_user(user):
    try:
        reader = Reader.objects.get(user = user)
    except reader.DoesNotExist:
        return READER_DOES_NOT_EXIST_RESPONSE
    try:
        librarian = Librarian.objects.get(reader = reader)
    except Librarian.DoesNotExist:
        return LIBRARIAN_DOES_NOT_EXIST_RESPONSE
    return derive_library_from_librarian(librarian)