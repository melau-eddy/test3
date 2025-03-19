from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Bus, Route, Schedule, Booking, Payment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# View to list all buses

def home(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('login_view')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'bus_list.html', {'buses': buses})


# View to show details of a specific bus
def bus_detail(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    # Generate a range of seat numbers (1 to total_seats)
    seat_range = range(1, bus.total_seats + 1)
    
    # Get all booked seats for this bus
    booked_seats = Booking.objects.filter(schedule__bus=bus).values_list('seats_booked', flat=True)
    
    # Define window seats (e.g., seats 1, 4, 5, 8, 9, 12, etc.)
    window_seats = []
    for i in range(0, bus.total_seats, 4):
        window_seats.append(i + 1)  # Left window seat
        window_seats.append(i + 4)  # Right window seat
    
    return render(request, 'bus_detail.html', {
        'bus': bus,
        'seat_range': seat_range,
        'booked_seats': booked_seats,
        'window_seats': window_seats,
    })


# View to list all schedules for a specific route
def schedule_list(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    schedules = Schedule.objects.filter(
        route__source__iexact=source,
        route__destination__iexact=destination,
        departure_time__date=date
    )
    return render(request, 'schedule_list.html', {'schedules': schedules})


# View to book a bus
@login_required(login_url='login_view')
def booking_create(request, bus_id, seat_number):
    bus = get_object_or_404(Bus, id=bus_id)
    schedule = Schedule.objects.filter(bus=bus).first()  # Assuming one schedule per bus for simplicity

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            schedule=schedule,
            seats_booked=seat_number,
            total_price=schedule.price  # Assuming price per seat
        )

        messages.success(request, 'Booking successful!')
        return redirect('booking_list')

    return render(request, 'booking_create.html', {
        'bus': bus,
        'seat_number': seat_number,
        'schedule': schedule,
    })

# View to list all bookings for the logged-in user
@login_required(login_url='login_view')
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})


# View to cancel a booking
@login_required(login_url='login_view')
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    schedule = booking.schedule

    if request.method == 'POST':
        # Refund seats
        schedule.available_seats += booking.seats_booked
        schedule.save()

        # Delete the booking
        booking.delete()

        messages.success(request, 'Booking cancelled successfully.')
        return redirect('booking_list')

    # If it's a GET request, show the confirmation page
    return render(request, 'booking_confirm_delete.html', {'booking': booking})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')