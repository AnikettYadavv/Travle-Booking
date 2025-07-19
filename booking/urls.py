from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('travel-info/<int:travel_id>/', views.travel_info, name='travel_info'),  
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'), 
    path('', views.home, name='home'), 
]