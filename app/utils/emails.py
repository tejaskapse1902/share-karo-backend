import requests
import os
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "email": FROM_EMAIL
        },
        "to": [
            {"email": to_email}
        ],
        "subject": "Your OTP for Password Reset",
        "htmlContent": f"""
        <p>Hello,</p>
        <p>Your OTP for password reset is:</p>
        <h2>{otp}</h2>
        <p>This OTP is valid for 5 minutes.</p>
        <p>Do not share it with anyone.</p>
        <p>Regards,<br>Your App Team</p>
        """
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(f"Brevo API error: {response.text}")
