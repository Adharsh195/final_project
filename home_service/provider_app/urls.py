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
from .views import *
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('provider_bookings/',views.provider_bookings, name='provider_bookings'),
    path('booking/<int:booking_id>/complete/',views.update_confirmed_booking_status,name='update_confirmed_booking_status'),
    path('booking/<int:booking_id>/<str:action>/',views.update_booking_status,name='update_booking_status'),
    path('provider_new_bookings/', views.provider_new_bookings, name='provider_new_bookings'),
    path('provider_confirmed_bookings/', views.provider_confirmed_bookings, name='provider_confirmed_bookings'),
    path('profile/', views.provider_profile, name='provider_profile'),
    path('profile/edit/', views.edit_provider_profile, name='edit_provider_profile'),
    path('reviews/', views.provider_reviews, name='provider_reviews'),
]

