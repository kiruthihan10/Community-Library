from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:user_name>/', views.detail, name='detail')
]