from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Provider

def provider_register(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        Provider.objects.create(
            user=user,
            company_name=request.POST['company'],
            phone=request.POST['phone'],
            address=request.POST['address']
        )
        return redirect('login')
    return render(request, 'provider_register.html')

from .models import Service, Provider
from django.contrib.auth.decorators import login_required

@login_required
def add_service(request):
    provider = Provider.objects.get(user=request.user)

    if request.method == "POST":
        Service.objects.create(
            provider=provider,
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price']
        )
        return redirect('provider_services')

    return render(request, 'add_service.html')


from django.contrib.auth.decorators import login_required
from bookings_app.models import Booking
from provider_app.models import ProviderService


@login_required
def provider_bookings(request):
    provider = request.user.provider
    bookings = Booking.objects.filter(
        provider_service__provider=provider,
        status="Completed"
    ).order_by('-booking_date')

    return render(request, 'provider_bookings.html', {
        'bookings': bookings
    })


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

@login_required
def update_booking_status(request, booking_id, action):
    provider = request.user.provider

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider_service__provider=provider
    )

    if action == "Accepted" and booking.status == "Pending":
        booking.status = "Confirmed"

    elif action == "Rejected" and booking.status == "Pending":
        booking.status = "Rejected"

    booking.save()
    return redirect("provider_new_bookings")


@login_required
def update_confirmed_booking_status(request, booking_id):
    provider = request.user.provider

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider_service__provider=provider,
        status="Confirmed",
    )

    booking.status = "Completed"
    booking.save()

    return redirect("provider_confirmed_bookings")



def provider_new_bookings(request):
    provider = request.user.provider
    bookings = Booking.objects.filter(
        provider_service__provider=provider,
        status='Pending')
    return render(request, 'provider_new_bookings.html', {
        'bookings': bookings
    })


def provider_confirmed_bookings(request):
    provider = request.user.provider
    bookings = Booking.objects.filter(
        provider_service__provider=provider,
        status='Confirmed')
    return render(request, 'provider_confirmed_bookings.html', {
        'bookings': bookings
    })

from django.shortcuts import render, get_object_or_404
from .models import Provider, ProviderService

def provider_profile(request):
    provider = get_object_or_404(Provider, user=request.user)
    services = ProviderService.objects.filter(provider=provider)

    context = {
        'provider': provider,
        'services': services
    }
    return render(request, 'profile.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Provider, ProviderService
from .forms import ProviderEditForm, ProviderServicePriceForm

def edit_provider_profile(request):
    provider = get_object_or_404(Provider, user=request.user)
    services = ProviderService.objects.filter(provider=provider)

    if request.method == 'POST':
        profile_form = ProviderEditForm(request.POST, instance=provider)

        if profile_form.is_valid():
            profile_form.save()

        for service in services:
            price_form = ProviderServicePriceForm(
                request.POST,
                instance=service,
                prefix=str(service.id)
            )
            if price_form.is_valid():
                price_form.save()

        return redirect('provider_profile')

    else:
        profile_form = ProviderEditForm(instance=provider)
        price_forms = [
            ProviderServicePriceForm(instance=s, prefix=str(s.id))
            for s in services
        ]

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'price_forms': zip(services, price_forms)
    })




from django.db.models import Avg
from user_app.models import Review

@login_required
def provider_reviews(request):
    provider = request.user.provider  

    reviews = Review.objects.filter(
        provider_service__provider=provider
    ).select_related('user', 'provider_service')

    average_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    context = {
        'reviews': reviews,
        'average_rating': average_rating
    }
    return render(request, 'provider_reviews.html', context)