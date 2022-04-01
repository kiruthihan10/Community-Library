from django.http import HttpResponse
from rest_framework import status

BAD_REQUEST_METHOD_RESPONSE = HttpResponse('Bad Request Method', status=status.HTTP_400_BAD_REQUEST)
INTERNAL_SERVER_ERROR = HttpResponse('Server Error',status=status.HTTP_500_INTERNAL_SERVER_ERROR)