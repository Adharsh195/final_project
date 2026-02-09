from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from .models import Booking
from provider_app.models import Service
from django.contrib.auth.decorators import login_required
from .models import Service
from django.shortcuts import get_object_or_404, redirect
from provider_app.models import ProviderService
import razorpay

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})


from django.db.models import Avg
from provider_app.models import ProviderService

def provider_list(request, service_id):
    providers = ProviderService.objects.filter(
        service_id=service_id
    ).select_related('provider').annotate(
        avg_rating=Avg('review__rating')
    )

    return render(request, 'provider_list.html', {
        'providers': providers
    })

@login_required
def book_service(request, provider_service_id):
    provider_service = get_object_or_404(ProviderService, id=provider_service_id)

    if request.method == "POST":
        booking = Booking.objects.create(
            user=request.user,
            provider_service=provider_service,
            customer_name=request.POST["customer_name"],
            customer_phone=request.POST["customer_phone"],
            customer_address=request.POST["customer_address"],
            booking_date=request.POST["booking_date"],
        )

        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
        )

        amount = int(provider_service.price * 100)

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        booking.razorpay_order_id = order["id"]
        booking.save()

        return render(request, "razorpay_checkout.html", {
            "booking": booking,
            "order": order,
            "razorpay_key": settings.RAZOR_KEY_ID,
            "amount": amount
        })

    return render(request, "book_service.html", {
        "provider_service": provider_service
    })



@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


razorpay_client=razorpay.Client(
    auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET)
)


def pay_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
    )

    amount = int(booking.provider_service.price * 100) 

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    booking.razorpay_order_id = order["id"]
    booking.save()

    context = {
        "booking": booking,
        "razorpay_key": settings.RAZOR_KEY_ID,
        "razorpay_order_id": order["id"],
        "amount": amount,
    }

    return render(request, "payment.html", context)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")

        booking = Booking.objects.get(razorpay_order_id=order_id)
        booking.razorpay_payment_id = payment_id
        booking.payment_status = "Paid"
        booking.save()

        return redirect("service_list")
    
