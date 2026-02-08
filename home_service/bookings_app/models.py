
from django.db import models
from django.contrib.auth.models import User
from provider_app.models import Service
from provider_app.models import ProviderService
from provider_app.models import Provider


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider_service = models.ForeignKey(ProviderService, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_phone = models.CharField(max_length=15)

    booking_date = models.DateTimeField()

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
        ('Cancelled','Cancelled'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_signature=models.CharField(max_length=200,blank=True,null=True)

    payment_status=models.CharField(
        max_length=20,
        choices=(('PENDING','PENDING'),('PAID','PAID')),
        default='PENDING'
    )
    

    def __str__(self):
        return f"{self.customer_name} - {self.service.name}"
    


