import requests
from django.conf import settings
from payrent.models import SMSLog

def send_sms(phone_number, message):
    if not phone_number.startswith("+"):
        phone_number = "+63" + phone_number.lstrip("0")

    url = "https://api.semaphore.co/api/v4/messages"
    payload = {
        "apikey": settings.SEMAPHORE_API_KEY,
        "number": phone_number,
        "message": message,
        "sendername": settings.SEMAPHORE_SENDER_NAME,
    }

    response = requests.post(url, data=payload)

    SMSLog.objects.create(
        recipient=phone_number,
        message=message,
        status="Sent" if response.status_code == 200 else f"Failed: {response.text}"
    )

    return response.json() if response.status_code == 200 else {"error": response.text}
#     return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)
#