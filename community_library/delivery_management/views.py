from django.shortcuts import render
from django.http import JsonResponse

from community_library.validate_and_extract import *

from book_management.validate_and_extract import *
from book_management.models import Book

from user_management.validate_and_extract import *
from user_management.models import Reader

from .models import *
from .serializers import RequestSerializer
from .validate_and_extract import *

from datetime import date, timedelta

def borrowel_view(request):
    if request.method == 'GET':
        borrowels = Borrowel.objects.all()
        serializers = BorrowelSerializers(instance = borrowels)
        return JsonResponse(serializers.data, status = status.HTTP_200_OK)
    return BAD_REQUEST_METHOD_RESPONSE

def request_book_by_user(request, book_id, user_id):
    if request.method == 'POST':
        user, book = extract_user_and_book(user_id, book_id)
        if type(book) == Book :
            if type(user) == Reader:
                try:
                    book_request = Request(
                        user = reader,
                        book = book
                    )
                except KeyError:
                    return KEYS_MISSING_RESPONSE
                book_request.save()
                serializer = RequestSerializer(instance = book_request)
                return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
            return user
        return book
    elif request.method == 'DELETE':
        user, book = extract_user_and_book(user_id, book_id)
        if type(book) == Book:
            if type(user) == Reader:
                book_request = extract_request(user, book)
                if type(book_request) == Request:
                    request.delete()
                    serializer = RequestSerializer(instance = request)
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
                return book_request
            return user
        return book
    return BAD_REQUEST_METHOD_RESPONSE

def request_books(request, book_id):
    book = extract_book(book_id)
    if type(book) == Book:
        book_requests = Request.objects.filter(book = book)
        serializer = RequestSerializer(instance = book_requests)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return book

def delivery_confirmed(request, book_id, user_id):
    if request.method != 'POST':
        return BAD_REQUEST_METHOD_RESPONSE
    request = extract_request_from_id(user_id, book_id)
    if type(request) == Request:
        request.delete()
        borrowel = Borrowel(
            book = book,
            reader = user,
            start_quality = book.quality,
        )
        borrowel.save()
    return request
    
def due_date(request, book_id, user_id):
    if request.method == 'GET':
        book_request = extract_request_from_id(user_id, book_id)
        if type(book_request) == Request:
            serializer = BorrowelDueSerializer(instance = book_request)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        return book_request
    elif request.method == 'PUT':
        book_request = extract_request_from_id(user_id, book_id)
        if type(book_request) == Request:
            book_request.extend_permite_day()
            book_request.save()
            serializer = BorrowelDueSerializer(instance = book_request)
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return book_request
    return BAD_REQUEST_METHOD_RESPONSE

def warning(request, book_id, user_id):
    if request.method == 'GET':
        book_request = extract_request_from_id(user_id, book_id)
        if type(book_request) == Request:
            return JsonResponse({'overpassed':date.today() > request.deadline}, status = status.HTTP_200_OK)
        return book_request
    return BAD_REQUEST_METHOD_RESPONSE

def extend(request, book_id):
    if request.method != 'POST':
        return BAD_REQUEST_METHOD_RESPONSE
    book = extract_book(book_id)
    if type(book) == Book:
        book_request = extract_request(request.user, book)
        if type(book_request) == Request:
            extend = BorrowelExtend(book_request)
            extend.save()
            serializer = ExtendSerializers(instance = extend)
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return book_request
    return book



# Create your views here.
