from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_view),
    path('info/<int:book_id>/',views.book_info),
    path('filter/',views.book_filter),
    path('holder/<int:book_id>/',views.book_holder),
    path('history/<int:book_id>/',views.book_history),
    path('wishlist/',views.wishlist_view)
]