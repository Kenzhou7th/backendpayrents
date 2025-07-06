from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.hashers import make_password

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

class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.EmailField(max_length=100, unique=True)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    password = models.CharField(max_length=100)
    date_occupancy = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tenants')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Report(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Rent(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rents')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rents')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rent for {self.tenant} - ₱{self.amount} due {self.due_date}"

class SMSLog(models.Model):
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.status}"