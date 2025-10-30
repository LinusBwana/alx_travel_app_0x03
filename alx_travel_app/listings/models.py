from django.db import models
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import date

# Create your models here.
class Property(models.Model):
    property_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    pricepernight = models.DecimalField(max_digits=10, decimal_places=2, 
                                        validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.location}"
    

class Booking(models.Model):
    status_choices = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "canceled"),
    ]
    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                      validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError('End date must be after start date')
            if self.start_date < date.today():
                raise ValidationError('Start date cannot be in the past')

    def __str__(self):
        return f"Booking {self.booking_id} - {self.property.name}"


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can only review a property once
        unique_together = ['property', 'user']

    def __str__(self):
        return f"Review by {self.user.username} for {self.property.name} - {self.rating}/5"
    

class Payment(models.Model):
    payment_choices = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "canceled"),
    ]
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_status=models.CharField(
        max_length=10,
        choices=payment_choices,
        default='pending'
    )
    amount=models.DecimalField(max_digits=10, decimal_places=2,
                               validators=[MinValueValidator(Decimal('0.01'))])
    transaction_id=models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.booking_id} - {self.payment_status}"