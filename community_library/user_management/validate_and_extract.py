from .models import Reader, Librarian

from community_library.validate_and_extract import *

from django.contrib.auth.models import User

from rest_framework import status

USER_DOES_NOT_EXIST_RESPONSE = HttpResponse('user does not exist',status=status.HTTP_404_NOT_FOUND)
READER_DOES_NOT_EXIST_RESPONSE = HttpResponse('reader does not exist',status=status.HTTP_404_NOT_FOUND)
LIBRARIAN_DOES_NOT_EXIST_RESPONSE = HttpResponse('Librarian Does Not Exist', status=status.HTTP_404_NOT_FOUND)
UNAUTH_RESPONSE = HttpResponse('Not Authorized', status= status.HTTP_401_UNAUTHORIZED)
DELIVERYMAN_DOES_NOT_EXIST = HttpResponse('Delivery Man Does Not Exist', status=status.HTTP_404_NOT_FOUND)

def validate_and_extract_reader(request, user_name):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    return extract_reader(user_name)

def extract_reader(user_name):
    if type(user_name) == User:
        user = user_name
    else:
        try:
            user = User.objects.get(username=user_name)   
        except User.DoesNotExist:
            return USER_DOES_NOT_EXIST_RESPONSE
    try:
        reader = Reader.objects.get(user=user)
    except Reader.DoesNotExist:
        return READER_DOES_NOT_EXIST_RESPONSE
    return reader

def extract_librarian(user_name):
    reader = extract_reader(user_name)
    if type(reader) == Reader:
        try:
            librarian = Librarian.objects.get(user=reader)
        except Librarian.DoesNotExist:
            return UNAUTHORIZED_ACCESS_RESPONSE
        return librarian
    return reader

def extract_deliveryman(user):
    reader = extract_reader(user)
    if type(reader) == Reader:
        try:
            deliveryman = DeliveryMan.objects.get(reader = reader)
        except DeliveryMan.DoesNotExist:
            return DELIVERYMAN_DOES_NOT_EXIST
        return deliveryman
    return reader

