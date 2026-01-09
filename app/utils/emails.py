import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("BREVO_SMTP_SERVER")
SMTP_PORT = int(os.getenv("BREVO_SMTP_PORT"))
SMTP_USERNAME = os.getenv("BREVO_SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP for Password Reset"
    body = f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.

Regards,
Your App Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
