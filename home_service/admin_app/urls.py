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
from . import views

urlpatterns = [
    path('view_providers/<int:service_id>/',views.view_providers,name='view_providers'),
    path('view_services',views.view_services,name='view_services'),
    path('admin/', admin.site.urls),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('add_service',views.add_service,name='add_service'),
    path('add_provider', views.add_provider, name='add_provider'),
    path('provider/delete/<int:id>/', views.delete_provider, name='delete_provider'),
    # path('provider/<int:provider_id>/bookings/', views.provider_bookings, name='view_bookings'),
    path('view_bookings/<int:provider_id>/',views.view_bookings,name='view_bookings'),
    path('admin_edit_provider_profile/<int:provider_service_id>/',views.admin_edit_provider_profile,name='admin_edit_provider_profile'),
    path("delete-service/<int:service_id>/",views.admin_delete_service,name="admin_delete_service"),
    path('logout_view', views.logout_view, name='logout_view'),
]
