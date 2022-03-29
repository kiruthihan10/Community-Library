from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Reader
from django.http import JsonResponse,HttpResponse

def index(request):
    if request.method == 'POST':
        data = request.POST
        if ('username' not in data.keys()) or ('password' not in data.keys()):
            return HttpResponse('Data Partially or Completely Missing',status=400)
        user = User.objects.create_user(
            username = data['username'],
            password = data['password']
        )
        reader = Reader(user,data['address'])
        reader.save()
        return HttpResponse(f'{data.username} successfully added',status=201)
    if request.method == 'GET':
        users = Reader.objects.all()
        users_list = [str(user) for user in users]
        return JsonResponse({'users':users_list}, status = 200)
    return HttpResponse('Wrong Request Method Use either GET or POST', status=400)

def detail(request, user_name):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=user_name).__dict__
            del user['_state']
            print(user)
            return JsonResponse(user, status=200)
        except User.DoesNotExist:
            return HttpResponse(f'{user_name} does not exist',status=404)
    return HttpResponse('Wrong Request Method Use GET', status=400)
        
def rating(request, user_name):
    if request.method == 'GET':
        try:
            user = Reader.objects.get(username=user_name)
            print(user)
            return JsonResponse({'rating':user.ratings}, status=200)
        except User.DoesNotExist:
            return HttpResponse(f'{user_name} does not exist',status=404)
    return HttpResponse('Wrong Request Method Use GET', status=400)
# Create your views here.
