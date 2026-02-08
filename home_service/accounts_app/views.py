from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, render

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("login")

        try:
            User.objects.create_user(
                username=username,
                password=password
            )
        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect("user_register")

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, "user_register.html")



from provider_app.models import Provider, Service, ProviderService

def provider_register(request):
    services = Service.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        company = request.POST['company']
        phone = request.POST['phone']
        address = request.POST['address']

        service_id = request.POST.get('service')  
        price = request.POST.get('price')         

        if not service_id or not price:
            messages.error(request, "Please select a service and enter price")
            return redirect('provider_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('provider_register')

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
        return redirect('login')

    return render(request, 'provider_register.html', {
        'services': services
    })

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # 🔐 ADMIN LOGIN
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')   # your admin dashboard URL name

            # 🧑‍🔧 PROVIDER LOGIN
            elif hasattr(user, 'provider'):
                return redirect('provider_dashboard')

            # 👤 NORMAL USER LOGIN
            else:
                return redirect('user_dashboard')

        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def provider_dashboard(request):
    return render(request, 'provider_dashboard.html')


from django.shortcuts import render, redirect, get_object_or_404
from bookings_app.models import Booking
from provider_app.models import ProviderService
from django.contrib.auth.decorators import login_required

@login_required
def book_service(request, provider_id):
    provider_service = get_object_or_404(
        ProviderService, id=provider_id
    )

    if request.method == "POST":
        Booking.objects.create(
            user=request.user,                    
            service=provider_service.service,       
            status='Pending'                        
        )
        return redirect('service_list')

    return render(
        request,
        'book_service.html',
        {'provider': provider_service}
    )


def home(request):
    return render(request,'home.html')