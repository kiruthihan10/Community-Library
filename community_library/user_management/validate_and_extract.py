from .models import Reader, Librarian

from community_library.validate_and_extract import *

from django.contrib.auth.models import User

from rest_framework import status

USER_DOES_NOT_EXIST_RESPONSE = HttpResponse('user does not exist',status=status.HTTP_204_NO_CONTENT)
READER_DOES_NOT_EXIST_RESPONSE = HttpResponse('reader does not exist',status=status.HTTP_204_NO_CONTENT)
LIBRARIAN_DOES_NOT_EXIST_RESPONSE = HttpResponse('Librarian Does Not Exist', status=status.HTTP_204_NO_CONTENT)
UNAUTH_RESPONSE = HttpResponse('Not Authorized', status= status.HTTP_401_UNAUTHORIZED)

def validate_and_extract_reader(request, user_name):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    return extract_reader(user_name)

def extract_reader(user_name):
    try:
        user = User.objects.get(username=user_name)
        reader = Reader.objects.get(user=user)
    except User.DoesNotExist:
        return USER_DOES_NOT_EXIST_RESPONSE
    except Reader.DoesNotExist:
        return READER_DOES_NOT_EXIST_RESPONSE
    return reader

def extract_librarian(user_name):
    reader = extract_reader(user_name)
    if type(reader) == Reader:
        try:
            librarian = Librarian.objects.get(user=reader)
        except Librarian.DoesNotExist:
            return LIBRARIAN_DOES_NOT_EXIST_RESPONSE
        return librarian
    return reader