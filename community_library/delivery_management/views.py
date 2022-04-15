from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from community_library.validate_and_extract import *

from book_management.validate_and_extract import *
from book_management.models import Book

from library_management.models import Library
from library_management.validate_and_extract import *

from user_management.validate_and_extract import *
from user_management.models import Reader, DeliveryMan

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

@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def request_book_by_user(request, book_id, user_id):
    if request.method == 'POST':
        if (user_id != request.user.username):
            return UNAUTH_RESPONSE
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
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    book = extract_book(book_id)
    if type(book) == Book:
        book_requests = Request.objects.filter(book = book)
        serializer = RequestSerializer(instance = book_requests)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return book

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delivery_confirmed(request, book_id, user_id):
    deliveryman = extract_deliveryman(request.user)
    if type(deliveryman) == DeliveryMan:
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
    return deliveryman

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated, )) 
def due_date(request, book_id, user_id):
    if request.method == 'GET':
        borrowel = extract_borrowel(user_id, book_id)
        if type(borrowel) == Borrowel:
            serializer = BorrowelDueSerializer(instance = borrowel)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        return borrowel
    elif request.method == 'PUT':
        librarian = extract_librarian(request.user)
        book = extract_book(book_id)
        if book.library.librarian == librarian:
            borrowel = Borrowel.objects.get(book = book, reader = extract_reader(user_id), return_date__isnull=True)
            borrowel.extend_permite_day()
            borrowel.due_extended = False
            borrowel.save()
            serializer = BorrowelDueSerializer(instance = borrowel)
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return book_request
    return BAD_REQUEST_METHOD_RESPONSE

def warning(request, book_id, user_id):
    if request.method == 'GET':
        borrowel = extract_borrowel(user_id, book_id)
        if type(borrowel) == Borrowel:
            return JsonResponse({'overpassed':date.today() > borrowel.deadline}, status = status.HTTP_200_OK)
        return borrowel
    return BAD_REQUEST_METHOD_RESPONSE

@api_view(['POST'])
@permission_classes((IsAuthenticated, )) 
def extend(request, book_id):
    if request.method != 'POST':
        return BAD_REQUEST_METHOD_RESPONSE
    book = extract_book(book_id)
    if type(book) == Book:
        borrowel = Borrowel.objects.filter(return_date__isnull=True, book = book)
        if borrowel.exists():
            if borrowel.reader == request.user:
                borrowel.due_extended = True
                borrowel.save()
                serilizer = BorrowelSerializers(instance = borrowel)
                return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
            return UNAUTHORIZED_ACCESS_RESPONSE
        return REQUEST_DOES_NOT_EXIST_RESPONSE
    return book

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def demand_view(request):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    librarian = extract_librarian(request.user)
    if type(librarian) == Librarian:
        library = derive_library_from_librarian(librarian)
        if type(library) == Library():
            books = Books.objects.filter(library = library)
            book_request = Request.objects.filter(book = books)
            serializer = RequestSerializer(instance = book_request)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        return library
    return librarian

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def demand_view_book(request, book_id):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    librarian = extract_librarian(request.user)
    if type(librarian) == Librarian:
        book = extract_book(book_id)
        if type(book) == Book:
            if authenticate_librarian(librarian, book):
                book_request = Request.objects.filter(book = book)
                serializer = RequestSerializer(instance = book_request)
                return JsonResponse(serializer.data, status = status.HTTP_200_OK)
            return UNAUTHORIZED_ACCESS_RESPONSE
        return book
    return librarian

@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def delete_demand(request, book_id, user_id):
    librarian = extract_librarian(request.user)
    if type(librarian) == Librarian:
        book = extract_book(book_id)
        if type(book) == Book:
            if authenticate_librarian(librarian, book):
                reader = extract_reader(user_id)
                if type(reader) == Reader:
                    try:
                        book_request = Request.objects.get(book = book, reader = reader)
                    except Request.DoesNotExist:
                        return REQUEST_DOES_NOT_EXIST_RESPONSE
                    book_request.delete()
                    serializer = RequestSerializer(instance = book_request)
                    return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
                return reader
            return UNAUTHORIZED_ACCESS_RESPONSE
        return book
    return librarian

def availability(request):
    if request.method == 'GET':
        books = Book.objects.all()
        taken_books = Borrowel.objects.filter(return_date__isnull=True)
        free_books = books and not taken_books
        serializer = BookSerializer(free_books)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    return BAD_REQUEST_METHOD_RESPONSE

def book_availability(request, book_id):
    if request.method == 'GET':
        book = extract_book(book_id)
        if type(book) == Book:
            borrowel = Borrowel.objects.filter(book = book, return_date__isnull=True)
            return JsonResponse({'availability':not borrowel.exist}, status = status.HTTP_200_OK)
        return book
    return BAD_REQUEST_METHOD_RESPONSE

def book_collection(request):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    borrowels = Borrowel.objects.filter(return_data__lte = date.today())
    serializer = BorrowelSerializers(instance = borrowels)
    return JsonResponse(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def notification(request):
    if request.method == 'GET':
        reader = extract_reader(request.user)
        if type(reader) == Reader:
            notifications = Notification.objects.filter(user = reader)
            serializer = NotificationSerializer(instance = notifications)
            return JsonResponse(serilizer.data, status = status.HTTP_200_OK)
        return reader
    return BAD_REQUEST_METHOD_RESPONSE

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def sepcific_notification(request, user_id):
    if request.method != 'POST':
        return BAD_REQUEST_METHOD_RESPONSE
    librarian = extract_librarian(request.user)
    if type(librarian) == Librarian:
        reader = extract_reader(user_id)
        if type(reader) == Reader:
            notifications = Notification.objects.filter(user = reader)
            serializer = NotificationSerializer(instance = notifications)
            return JsonResponse(serilizer.data, status = status.HTTP_200_OK)
        return reader
    return librarian


def complaints(request):
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    complaints = Complaints.objects.all()
    serializer = ComplaintSerializer(instance = complaints)
    return JsonResponse(serializer.data , status = status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated, ))
def specific_complaint(request, user_id):
    if request.method == 'GET':
        deliveryman = extract_deliveryman(user_id)
        if type(deliveryman) != DeliveryMan:
            return deliveryman
        complaints = Complaints.objects.filter(on = deliveryman)
        serializer = ComplaintSerializer(instance = complaints)
        return JsonResponse(serializer.data , status = status.HTTP_200_OK)
    elif request.method == 'POST':
        deliveryman = extract_deliveryman(user_id)
        if type(deliveryman) != DeliveryMan:
            return deliveryman
        reader = extract_reader(request.user)
        if type(reader) != Reader:
            return reader
        complaint = Complaints(
            by = reader,
            on = deliveryman,
        )
        complaint.save()
        serializer = ComplaintSerializer(instance = complaint)
        return JsonResponse(serializer.data , status = status.HTTP_201_CREATED)
    return BAD_REQUEST_METHOD_RESPONSE

# Create your views here.
