from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.hashers import make_password

# Room Model
class Room(models.Model):
    pad_number = models.CharField(max_length=50)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    one_month_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    one_month_advance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_water_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_electric_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    initial_electric_reading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    initial_water_reading = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Room {self.pad_number}"

# Tenant Model
class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    password = models.CharField(max_length=100)
    date_occupancy = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tenants')

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash the password for new tenants
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Notification Model
class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Report Model
class Report(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from rest_framework import serializers

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
