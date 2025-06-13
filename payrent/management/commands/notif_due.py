from django.core.management.base import BaseCommand
from payrent.models import Rent
from django.utils import timezone
from datetime import timedelta
from payrent.utils.sms import send_sms

class Command(BaseCommand):
    help = 'Notify tenants X days before due date'

    def handle(self, *args, **kwargs):
        target_date = timezone.now().date() + timedelta(days=3)
        due_rents = Rent.objects.filter(due_date=target_date)

        for rent in due_rents:
            tenant = rent.tenant
            phone = tenant.contact_number
            message = f"Reminder: Your rent of ₱{rent.amount} is due on {rent.due_date}. – PayRent"
            send_sms(phone, message)
            self.stdout.write(self.style.SUCCESS(f"Sent reminder to {tenant.first_name} at {phone}"))
