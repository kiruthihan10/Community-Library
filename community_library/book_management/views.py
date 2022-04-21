from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .validate_and_extract import *

from library_management.validate_and_extract import *
from library_management.models import Library
from library_management.serializers import *

from user_management.serializers import ReaderSerializer

from delivery_management.models import Borrowel

from community_library.validate_and_extract import *

def book_view_get():
    # RETURN LIST OF ALL THE BOOKS
    books = Book.objects.all()
    return serialize_book(books)

def book_view_post(request):
    ## CREATE A BOOK BY LIBRARIAN
    library = derive_library_from_user(request.user)
    if type(library) == Library:
        book = book_dict_extract(data, library)
        book.save()
        return serialize_book(book)
    return library

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def book_view(request):
    #BOOK RELATED CREATE AND READ OPERATIONS
    if request.method == 'GET':
        return book_view_get()
    elif request.method == 'POST':
        return book_view_post(request)
    else:
        return BAD_REQUEST_METHOD_RESPONSE

def book_info_get(book_id):
    # READ SINGLE BOOK INFORMATION
    book = extract_book(book_id)
    if type(book) == Book:
        return serialize_book(book)
    return book

def book_info_put(request, book_id):
    # UPDATE SINGLE BOOK INFORMATION BY LIBRARIAN
    data = request.data
    book = extract_book(book_id)
    if type(book) == Book:
        if authenticate_librarian_from_user(request.user, book):
            try:
                book.name = data['name']
                book.author = data['author']
                book.price = data['price']
                book.language = data['language']
                book.quality = data['quality']
                book.save()
            except KeyError:
                return HttpResponse("Data Missing", status = status.HTTP_206_PARTIAL_CONTENT)
            return serialize_book(book)
        return BOOK_DOES_NOT_BELONGS_TO_YOU
    return book

def book_info_delete(request, book_id):
    # DISCARD BOOK BY LIBRARIAN
    book = extract_book(book_id)
    if type(book) == Book:
        if authenticate_librarian_from_user(request.user, book):
            book.delete()
            return serialize_book(book)
        return BOOK_DOES_NOT_BELONGS_TO_YOU
    return book

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def book_info(request, book_id):
    # INDIVIDUAL BOOK BASED CRUD OPERATION
    if request.method == 'GET':
        return book_info_get(book_id)
    elif request.method == 'PUT':
        authenticate_librarian_from_user = (request, book)
        book_info_put(data, book_id)
    elif request.method == 'DELETE':
        book_info_delete(request, book_id)
    return BAD_REQUEST_METHOD_RESPONSE

def book_filter(request):
    # GET LIST OF BOOKS WITH THE GIVEN PARAMETERS FILTERED
    # PARAMETERS ARE PASSED VIA REQUEST DATA KEY VALUE PAIN
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    data = request.data
    keys = data.keys()
    library = extract_library(library_id) if 'library_id' in keys else None
    if type(library) != Library:
        return LIBRARY_DOES_NOT_EXIST_RESPONSE
    author = data['author'] if 'author' in keys else None
    price = data['price'] if 'price' in keys else None
    language = data['language'] if 'language' in keys else None
    quality = data['quality'] if 'quality' in keys else None
    ID = data['ID'] if ID in keys else None
    books = Book.objects().filter(
        ID = ID,
        author = author,
        name = name,
        price = price,
        language = language,
        quality = quality,
        library = library,
    )
    serializer = BookSerializer(instance = books)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def book_holder(request, book_id):
    # RETURN THE CURRENT HOLDER OF THE BOOK
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    book = extract_book(book_id)
    if type(book) == Book:
        if authenticate_librarian_from_user(request.user, book):
            try:
                borrowel = Borrowel.objects.get(book = book, return_date__isnull = True)
                reader = borrowel.reader
                serializer = ReaderSerializer(instance = reader)
            except Borrowel.DoesNotExist:
                library = borrowel.book.library
                serializer = LibrarySerializer(instance = library)
            return JsonResponse(serializer.data, status= status.HTTP_200_OK)
        return BOOK_DOES_NOT_BELONGS_TO_YOU
    return book

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def book_history(request, book_id):
    # RETURN THE LIST OF READERS WHO HAVE OBTAINED THE BOOK
    if request.method != 'GET':
        return BAD_REQUEST_METHOD_RESPONSE
    book = extract_book(book_id)
    if type(book) == Book:
        if authenticate_librarian_from_user(request.user, book):
            borrowel = Borrowel.objects.filter(book = book)
            serializer = BorrowelSerializer(instance = borrowel)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        return BOOK_DOES_NOT_BELONGS_TO_YOU
    return book
    
def wishlist_get(request):
    # RETURN THE WISHLIST OF THE REQUEST USER
    reader = extract_reader(request.user)
    if type(reader) == Reader:
        wishlist = Wishlist.objects.filter(reader = reader)
        serializer = WishListSerializer(instance = wishlist)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)
    return reader

def wishlist_post(request):
    # ADD A BOOK TO THE WISHLIST
    reader = extract_reader(request.user)
    if type(reader) == Reader:
        try:
            book_id = request.data['book']
        except KeyError:
            return KEYS_MISSING_RESPONSE
        book = extract_book(book_id)
        if type(book) == Book:
            wishlist = Wishlist(
                reader = reader,
                book = book
            )
            wishlist.save()
            serializer = WishListSerializer(instance = wishlist)
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return book
    return reader

def wishlist_delete(request):
    #DELETE A BOOK FORM WISHLIST
    reader = extract_reader(request.user)
    if type(reader) == Reader:
        try:
            book_id = request.data['book']
        except KeyError:
            return KEYS_MISSING_RESPONSE
        book = extract_book(book_id)
        if type(book) == Book:
            wishlist = Wishlist.objects.get(reader = reader, book = book)
            wishlist.delete()
            serializer = WishListSerializer(instance = wishlist)
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return book
    return reader

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def wishlist_view(request):
    # WISHLIST CRUD OPERATIONS
    if request.method == 'GET':
        wishlist_get(request)
    elif request.method == 'POST':
        wishlist_post(request)
    elif request.method == 'DELETE':
        wishlist_delete(request)
    return BAD_REQUEST_METHOD_RESPONSE
