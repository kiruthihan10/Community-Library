from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Reader
from .serializers import UserSerializer, ReaderSerializer

from django.contrib.auth.models import User, UserManager
from django.http import JsonResponse, HttpResponse

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

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

def specific_user_view(request, user_name):
    print(user_name)
    if request.method == 'GET':
        user = Reader.objects.get(user=User.objects.get(username=user_name))
        print(user.__dict__)
        return JsonResponse(ReaderSerializer(user).data, status = status.HTTP_200_OK)
    return HttpResponse('Bad Request Method', status=status.HTTP_400_BAD_REQUEST)