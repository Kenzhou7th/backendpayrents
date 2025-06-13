from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rent
from .utils.sms import send_sms

@receiver(post_save, sender=Rent)
def send_rent_sms(sender, instance, created, **kwargs):
    if created:
        tenant = instance.tenant
        message = f"Hi {tenant.first_name}, your rent of ₱{instance.amount} is due on {instance.due_date}. – PayRent"
        send_sms(tenant.contact_number, message)
