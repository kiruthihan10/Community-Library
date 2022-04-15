from django.urls import path

from . import views

urlpatterns = [
    path('', views.borrowel_view),
    path('Request/<int:book_id>',views.request_books),
    path('Request/<int:book_id>/<slug:user_name>',views.request_book_by_user),
    path('Delivered/<int:book_id>/<slug:user_name>',views.delivery_confirmed),
    path('Due/<int:book_id>/<slug:user_name>',views.due_date),
    path('Warning/<slug:user_name>',views.warning),
    path('Extend/<int:book_id>',views.extend),
    path('Demand',views.demand_view),
    path('Demand/<int:book_id>',views.demand_view_book),
    path('Demand/<int:book_id>/<slug:user_name>',views.delete_demand),
    path('Available',views.availability),
    path('Available/<int:book_id>',views.book_availability),
    path('Collection',views.book_collection),
    path('Notifications',views.notification),
    path('Notifications/<slug:user_name>',views.sepcific_notification),
    path('Complaints',views.complaints),
    path('Complaints/<slug:user_name>',views.specific_complaint),
]