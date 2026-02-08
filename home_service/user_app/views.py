from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bookings_app.models import Booking

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status='Completed'
    ).order_by('-booking_date')

    return render(request, 'user_bookings.html', {
        'bookings': bookings
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Review

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='Completed'  
    )

    if Review.objects.filter(booking=booking).exists():
        messages.warning(request, "You have already reviewed this service.")
        return redirect('user_bookings')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            provider_service=booking.provider_service,
            booking=booking,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Review submitted successfully!")
        return redirect('user_bookings')

    return render(request, 'add_review.html', {'booking': booking})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bookings_app.models import Booking


@login_required
def confirmed_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status='Confirmed'
    ).order_by('-booking_date')

    return render(request, 'confirmed_bookings.html', {
        'bookings': bookings
    })

@login_required
def Pending_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status='Pending'
    ).order_by('-booking_date')

    return render(request, 'Pending_bookings.html', {
        'bookings': bookings
    })


@login_required
def rejected_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        status='Rejected'
    ).order_by('-booking_date')

    return render(request, 'rejected_bookings.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == "Cancelled":
        return redirect("Pending_bookings")
    
    booking.status = "Cancelled"
    booking.save()

    return redirect("Pending_bookings")