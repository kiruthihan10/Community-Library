from .models import Request

from django.http import HttpResponse

from rest_framework import status

REQUEST_DOES_NOT_EXIST_RESPONSE = HttpResponse('Book Request does not exist', status=status.HTTP_204_NO_CONTENT)

def extract_request(user, book):
    try:
        request = Request.objects.get(user=user, book = book)
    except Request.DoesNotExist:
        return request

def extract_user_and_book(user_id, book_id):
    book = extract_book(book_id)
    user = extract_reader(user_id)
    return user, book

def extract_request_from_id(user_id, book_id):
    user, book = extract_user_and_book(user_id, book_id)
    if type(user) == Reader:
        return extract_request(user, book) if type(book) == Book else book
    return user
