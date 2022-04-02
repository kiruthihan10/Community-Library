from .models import Book
from .serializers import BookSerializer

from django.http import JsonResponse, HttpResponse

from rest_framework import status

BOOK_DOES_NOT_EXIST = HttpResponse('Book Does not Exist', status = status.HTTP_204_NO_CONTENT)
BOOK_DOES_NOT_BELONGS_TO_YOU = HttpResponse('Book Does not belongs to your library', status = status.HTTP_401_UNAUTHORIZED)
def serialize_book(book):
    serializer = BookSerializer(instance=book)
    return JsonResponse(serializer.data, status = status.HTTP_200_OK)

def book_dict_extract(data, library):
    return Book(
        name = data['name'],
        author = data['author'],
        price = data['price'],
        language = data['language'],
        quality = data['quality'],
        library = library
    )

def validate_and_extract_book(request, book_id):
    if request.method == 'GET':
        return extract_book(book_id)
        
def extract_book(book_id):
    try:
        return Book.objects.get(ID = book_id)
    except Book.DoesNotExist:
        return BOOK_DOES_NOT_EXIST

def authenticate_librarian(librarian, book):
    library = book.library
    return library.librarian == librarian

def authenticate_librarian_from_user(user, book):
    librarian = extract_librarian(user)
    return authenticate_librarian(librarian, book)