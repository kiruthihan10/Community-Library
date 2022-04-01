from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()

router.register(r'',views.UserViewSet,'user')

urlpatterns = [
    path('<slug:user_name>/',views.specific_user_view),
    path('<slug:user_name>/rating',views.rating_view),
    path('<slug:user_name>/member',views.member_view),
    path('<slug:user_name>/member/<int:library_id>',views.specific_member),
    path(r'', include(router.urls)),
]