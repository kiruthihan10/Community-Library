from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()

router.register(r'',views.UserViewSet,'user')

urlpatterns = [
    path('<slug:user_name>/',views.specific_user_view),
    path(r'', include(router.urls)),
]