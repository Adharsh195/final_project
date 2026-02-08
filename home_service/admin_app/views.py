from django.shortcuts import render,redirect

# Create your views here.
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

from provider_app.models import Service, Provider
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from provider_app.models import Service

def add_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Service.objects.create(name=name)
        return redirect('add_service')

    return render(request, 'add_service.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from provider_app.models import Provider, Service, ProviderService

def add_provider(request):
    services = Service.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        company = request.POST['company']
        phone = request.POST['phone']
        address = request.POST['address']

        service_id = request.POST.get('service')   # ✅ single service
        price = request.POST.get('price')          # ✅ single price

        if not service_id or not price:
            messages.error(request, "Please select a service and enter price")
            return redirect('add_provider')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('add_provider')

        user = User.objects.create_user(username=username, password=password)

        provider = Provider.objects.create(
            user=user,
            company_name=company,
            phone=phone,
            address=address
        )

        service = Service.objects.get(id=service_id)

        ProviderService.objects.create(
            provider=provider,
            service=service,
            price=price
        )

        messages.success(request, "Provider registered successfully")
        return redirect('admin_dashboard')

    return render(request, 'add_provider.html', {
        'services': services
    })


def view_services(request):
    services=Service.objects.all()
    return render(request,'view_services.html',{'services':services})

from django.db.models import Avg

def view_providers(request,service_id):
    providers = ProviderService.objects.filter(
        service_id=service_id
    ).select_related('provider').annotate(
        avg_rating=Avg('review__rating')
    )

    return render(request, 'view_providers.html', {'providers': providers})


from django.shortcuts import get_object_or_404, redirect
from provider_app.models import Provider

def delete_provider(request, id):
    provider = get_object_or_404(Provider, id=id)

    if request.method == "POST":
        provider.delete()
        return redirect('view_providers')  # change to your providers list URL name
    
from bookings_app.models import Booking

def view_bookings(request,provider_id):
    bookings=Booking.objects.filter(provider_service__provider__id=provider_id)
    return render(request,'view_bookings.html',{'bookings':bookings})





from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from provider_app.models import Provider, ProviderService
from provider_app.forms import ProviderEditForm, ProviderServicePriceForm

@staff_member_required   # ✅ only admin/staff allowed
def admin_edit_provider_profile(request, provider_service_id):
    provider_service = get_object_or_404(
        ProviderService,
        id=provider_service_id
    )
    provider = provider_service.provider

    services = ProviderService.objects.filter(provider=provider)

    if request.method == 'POST':
        profile_form = ProviderEditForm(request.POST, instance=provider)

        price_forms = [
            ProviderServicePriceForm(
                request.POST,
                instance=service,
                prefix=str(service.id)
            )
            for service in services
        ]

        if profile_form.is_valid() and all(pf.is_valid() for pf in price_forms):
            profile_form.save()
            for pf in price_forms:
                pf.save()
            return redirect('view_services')

    else:
        profile_form = ProviderEditForm(instance=provider)
        price_forms = [
            ProviderServicePriceForm(
                instance=service,
                prefix=str(service.id)
            )
            for service in services
        ]

    return render(request, 'edit_provider_profile.html', {
        'provider': provider,
        'profile_form': profile_form,
        'price_forms': zip(services, price_forms),
    })



@login_required
def admin_delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method=="POST":
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect("view_services")