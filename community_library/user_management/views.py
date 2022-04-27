from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Reader
from .serializers import *

from library_management.models import MemberShip, Library

from django.contrib.auth.models import User, UserManager
from django.http import JsonResponse, HttpResponse

from user_management.validate_and_extract import *
from community_library.validate_and_extract import *
from library_management.validate_and_extract import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid() and 'address' in data.keys():
            user = User.objects.create_user(data['username'],None,data['password'])
            reader = Reader(user=user,address=data['address'])
            reader.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        readers = Reader.objects.all()
        serializer = ReaderSerializer(readers)
        return Response(serializer.data)

def specific_user_get(user_name):
    ## READ specific user's informations
    try:
        user = Reader.objects.get(user=User.objects.get(username=user_name))
    except Reader.DoesNotExist:
        return READER_DOES_NOT_EXIST_RESPONSE
    except Exception:
        return INTERNAL_SERVER_ERROR
    reader = ReaderSerializer(user)
    return JsonResponse(reader.data, status = status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsAuthenticated, ))
def specific_user_put(request, user_name):
    ## UPDATE specific user's information
    request_user = request.user
    if request.user.username == user_name or request_user.is_superuser:
        try:
            user=User.objects.get(username=user_name)
        except User.DoesNotExist:
            return USER_DOES_NOT_EXIST_RESPONSE
        if 'password' in request.data.keys():
            user.set_password(request.data['password'])
            user.save()
        if 'address' in request.data.keys():
            try:
                reader = Reader.objects.get(user=user)
            except Reader.DoesNotExist:
                return READER_DOES_NOT_EXIST_RESPONSE
            reader.address = request.data['address']
            reader.save()
        return JsonResponse(ReaderSerializer(reader).data, status = status.HTTP_201_CREATED)
    return UNAUTH_RESPONSE

def specific_user_view(request, user_name):
    ## USER PARTIAL CRUD
    if request.method == 'GET':
        return specific_user_get(user_name)
    elif request.method == 'PUT':
        return specific_user_put(user_name)
    return BAD_REQUEST_METHOD_RESPONSE

def rating_view(request, user_name):
    ## Return rating information of a specific user given in URL parameter
    reader = validate_and_extract_reader(request, user_name)
    if type(reader) == Reader:
        serializer = ReaderRatingSerializer(instance=reader)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    return reader

def member_view(request, user_name):
    ## Return all the membership information of a specific user given in URL parameter
    reader = validate_and_extract_reader(request, user_name)
    if type(reader) == Reader:
        memberships = MemberShip.objects.filter(reader = reader)
        serializer = ReaderMemberSerializer(instance=memberships)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return reader

def specific_member_get(user_name, library_id):
    ## READ A SPECIFIC MEMBERSHIP DETAILS FOR A SPECIFIC USER & LIBRARY
    reader = extract_reader(user_name)
    if type(reader) == Reader:
        library = extract_library(library_id)
        print(library)
        if type(library) == Library:
            try:
                membership = MemberShip.objects.get(reader = reader, lib = library)
            except MemberShip.DoesNotExist:
                return MEMBERSHIP_DOES_NOT_EXIST_RESPONSE
            serializer = ReaderMemberSerializer(instance = membership)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return library
    return reader

def specific_member_post(user_name, library_id):
    ## CREATE NEW MEMBERSHIP FOR A SPECIFIC USER ON A SPECIFIC LIBRARY
    reader = extract_reader(user_name)
    if type(reader) == Reader:
        library = extract_library(library_id)
        if type(library) == Library:
            if not MemberShip.objects.filter(reader=reader,lib = library).exists():
                membership = MemberShip(
                    reader=reader,
                    lib=library).save()
                return JsonResponse(ReaderMemberSerializer(instance=membership).data, status = status.HTTP_201_CREATED)
            return HttpResponse("Membership Already Exists", status = status.HTTP_400_BAD_REQUEST)
        return library
    return reader

def specific_member_delete(user_name, library_id):
    ## DELETE A MEMBERSHIP OF A USER ON A LIBRARY
    reader = extract_reader(user_name)
    if type(reader) == Reader:
        library = extract_library(library_id)
        if type(library) == Library:
            membership = MemberShip.objects.filter(reader=reader,lib = library)
            if membership.exists():
                membership.delete()
                serializer = ReaderMemberSerializer(instance=membership)
                return JsonResponse(serializer.data, status = status.HTTP_200_OK)
            return MEMBERSHIP_DOES_NOT_EXIST_RESPONSE
        return library
    return reader

def specific_member(request, user_name, library_id):
    ## MEMBERSHIP PERTIAL CRUD OPERATIONS
    if request.method == 'GET':
        return specific_member_get(user_name, library_id)
    elif request.method == 'POST':
        return specific_member_post(user_name, library_id)
    elif request.method == 'DELETE':
        return specific_member_delete(user_name, library_id)
    return BAD_REQUEST_METHOD_RESPONSE

