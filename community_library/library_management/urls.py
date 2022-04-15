from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views


urlpatterns = [
    path('',views.library_view),
    path('<int:library_id>/',views.specific_library),
    path('<int:library_id>/librarian',views.specific_library_librarian),
    path('<int:library_id>/inventory',views.specific_library_inventory),
    path('<int:library_id>/ban/<slug:user_name>',views.specific_library_ban_user),
]