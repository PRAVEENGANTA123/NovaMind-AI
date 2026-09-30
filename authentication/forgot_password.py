"""
=========================================
NovaMind AI - Forgot Password Service
=========================================
"""

from datetime import datetime, timezone
from authentication.password import hash_password
from authentication.email_service import send_email
from authentication.email_templates import password_reset_email
from authentication.otp_service import generate_email_otp
from database.users import (
    get_user_by_email,
    verify_email_otp,
    update_password,
)


def send_password_reset_otp(email: str) -> tuple[bool, str]:
    """
    Generate and send a password reset OTP to the user's email.
    """
    email = (email or "").strip().lower()
    if not email:
        return False, "Please enter your registered email address."

    user = get_user_by_email(email)
    if not user:
        return False, "No account is registered with this email address."

    if not user.get("is_active", True):
        return False, "This account is inactive. Please contact support."

    otp = generate_email_otp(email)
    username = user.get("username", "User")
    html = password_reset_email(username=username, otp=otp)

    sent = send_email(
        recipient=email,
        subject="NovaMind AI - Password Reset Code",
        html=html
    )

    if not sent:
        return False, "Unable to send verification email. Please check your email configuration."

    return True, "A 6-digit verification code has been sent to your email."


def verify_otp_and_reset_password(
    email: str,
    otp: str,
    password: str,
    confirm_password: str,
) -> tuple[bool, str]:
    """
    Verify the reset OTP and safely update the user's password.
    """
    email = (email or "").strip().lower()
    otp = (otp or "").strip()

    if not email:
        return False, "Email address is required."

    if not otp:
        return False, "Please enter the 6-digit verification code."

    if len(otp) != 6 or not otp.isdigit():
        return False, "Verification code must be 6 digits."

    if not password:
        return False, "Please enter a new password."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    # Validate OTP against MongoDB record
    user = verify_email_otp(email, otp)
    if not user:
        return False, "Invalid or expired verification code. Please request a new code."

    # Hash new password with bcrypt salt and update database
    hashed_password = hash_password(password)
    update_password(email, hashed_password)

    return True, "Your password has been reset successfully! You can now log in."
