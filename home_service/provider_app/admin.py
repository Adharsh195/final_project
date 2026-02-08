from django.contrib import admin

# Register your models here.
# admin.py
from .models import Provider, Service,ProviderService
admin.site.register(Provider)
admin.site.register(Service)
admin.site.register(ProviderService)