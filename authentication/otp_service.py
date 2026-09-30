"""
=========================================
NovaMind AI - OTP Service
=========================================
"""

from datetime import datetime, timedelta, timezone

from authentication.email_service import send_email
from authentication.email_templates import otp_email
from database.users import (
    get_user_by_email,
    save_email_otp,
)
from utils.token import generate_otp


# =====================================
# Generate Email OTP
# =====================================

def generate_email_otp(email):
    """
    Generate a 6-digit OTP and save it to MongoDB.
    """

    otp = generate_otp()

    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    save_email_otp(
        email=email,
        otp=otp,
        expiry=expiry
    )

    return otp


# =====================================
# Resend Email OTP
# =====================================

def resend_email_otp(email):
    """
    Generate a new OTP and send it again.
    """

    user = get_user_by_email(email)

    if not user:
        return False, "User not found."

    otp = generate_email_otp(email)

    html = otp_email(
        username=user["username"],
        otp=otp
    )

    success = send_email(
        recipient=email,
        subject="NovaMind AI - Email Verification Code",
        html=html
    )

    if not success:
        return False, "Unable to send verification email."

    return True, "A new verification code has been sent."