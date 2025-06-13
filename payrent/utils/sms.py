import requests
from django.conf import settings

def send_sms(phone_number, message):
    url = "https://api.semaphore.co/api/v4/messages"

    payload = {
        "apikey": settings.SEMAPHORE_API_KEY,
        "number": phone_number,
        "message": message,
        "sendername": settings.SEMAPHORE_SENDER_NAME,
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
