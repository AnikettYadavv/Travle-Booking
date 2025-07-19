from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import TravelOption, Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm , CustomUserCreationForm
from django.contrib.auth.models import User 

# Homepage
def home(request):
    travel_options = TravelOption.objects.all()

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if destination:
        travel_options = travel_options.filter(destination__icontains=destination)
    if date:
        travel_options = travel_options.filter(date_time__date=date)

    return render(request, 'index.html', {'Home': travel_options})

# User Registration
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

#User Profile
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# Profile Update
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Travel Info
@login_required
def travel_info(request, travel_id):
    travel = get_object_or_404(TravelOption, pk=travel_id)
    if request.method == 'POST':
        seats = int(request.POST['seats'])
        if seats <= travel.available_seats:
            travel.available_seats -= seats
            travel.save()
            booking = Booking(user=request.user, travel_option=travel, number_of_seats=seats, total_price=seats * travel.price)
            booking.save()
            return redirect('view_bookings')
        else:
            return render(request, 'travel_info.html', {'travel': travel, 'error': 'Seats not available'})
    else:
        return render(request, 'travel_info.html', {'travel': travel })

# View Bookings
@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

# Cancel Booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.save()
        travel_option = booking.travel_option
        travel_option.available_seats += booking.number_of_seats
        travel_option.save()
    booking.delete()  
    return redirect('view_bookings')
