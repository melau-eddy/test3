from django.urls import path
from . import views
from .views import (
    bus_list, bus_detail, schedule_list,
    booking_create, booking_list, booking_delete
)

urlpatterns = [
    # Bus views
    path('buses/', bus_list, name='bus_list'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
<<<<<<< HEAD
    path('register/', views.register_view, name='register_view'),
=======
    path('register/', views.register, name='register'),
>>>>>>> ffef4652497431953d070e397f57e1f455123291
    path('buses/<int:pk>/', bus_detail, name='bus_detail'),

    # Schedule views
    path('schedules/', schedule_list, name='schedule_list'),

    # Booking views
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/new/', booking_create, name='booking_create'),
    path('bookings/<int:pk>/delete/', booking_delete, name='booking_delete'),
    path('bookings/new/<int:bus_id>/<int:seat_number>/', booking_create, name='booking_create'),
]
