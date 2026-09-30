"""
=========================================
NovaMind AI - Email Service
=========================================
"""

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


# ==========================================
# Email Configuration
# ==========================================

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


# ==========================================
# Send Email
# ==========================================

def send_email(
    recipient,
    subject,
    html
):
    """
    Send HTML Email
    """

    try:

        message = MIMEMultipart("alternative")

        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(
            MIMEText(
                html,
                "html"
            )
        )

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(message)

        return True

    except Exception as e:

        print(e)

        return False