"""
URL configuration for home_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from.import views

urlpatterns = [
    path('service_list',views.service_list,name='service_list'),
    path('provider_list/<int:service_id>/',views.provider_list,name='provider_list'),
    path('book/<int:provider_service_id>/', views.book_service, name='book_service'),
    path("pay/<int:booking_id>/", views.pay_booking, name="pay_booking"),
    path("payment-success/", views.payment_success, name="payment_success"),
]