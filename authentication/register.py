"""
=========================================
NovaMind AI - User Registration Service
=========================================
"""

from datetime import datetime

from email_validator import (
    validate_email,
    EmailNotValidError
)

from authentication.password import hash_password
from authentication.email_service import send_email
from authentication.email_templates import otp_email
from authentication.otp_service import generate_email_otp
from database.users import (
    email_exists,
    create_user
)


# =====================================
# Register User
# =====================================

def register_user(username, email, password, confirm_password):
    """
    Register a new user.

    Returns:
        (True, message)
        (False, message)
    """

    # =====================================
    # Clean Input
    # =====================================

    username = username.strip()
    email = email.strip().lower()

    # =====================================
    # Username Validation
    # =====================================

    if not username:
        return False, "Please enter your username."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    # =====================================
    # Email Validation
    # =====================================

    if not email:
        return False, "Please enter your email."

    try:
        validate_email(email)

    except EmailNotValidError:
        return False, "Please enter a valid email address."

    # =====================================
    # Password Validation
    # =====================================

    if not password:
        return False, "Please enter a password."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    # =====================================
    # Duplicate Email Check
    # =====================================

    if email_exists(email):
        return False, "An account already exists with this email."

    # =====================================
    # Create User Document
    # =====================================

    user = {

        # ---------------------------------
        # Basic Information
        # ---------------------------------

        "username": username,
        "email": email,
        "password": hash_password(password),

        # ---------------------------------
        # Account
        # ---------------------------------

        "role": "user",
        "status": "active",
        "is_active": True,
        "email_verified": False,

        # ---------------------------------
        # Email OTP
        # ---------------------------------

        "email_otp": None,
        "email_otp_expiry": None,

        # ---------------------------------
        # Password Reset
        # ---------------------------------

        "reset_token": None,
        "token_expiry": None,

        # ---------------------------------
        # Profile
        # ---------------------------------

        "profile_image": None,
        "bio": "",
        "location": "",
        "website": "",

        # ---------------------------------
        # Statistics
        # ---------------------------------

        "statistics": {
            "total_chats": 0,
            "total_pdfs": 0,
            "total_urls": 0,
            "total_messages": 0
        },

        # ---------------------------------
        # User Settings
        # ---------------------------------

        "settings": {
            "theme": "light",
            "language": "English",
            "default_model": "gemini",
            "temperature": 0.7
        },

        # ---------------------------------
        # Dashboard
        # ---------------------------------

        "favorites": [],
        "recent_chats": [],
        "bookmarks": [],

        # ---------------------------------
        # Dates
        # ---------------------------------

        "created_at": datetime.utcnow(),
        "last_login": None

    }

    # =====================================
    # Save User
    # =====================================

    create_user(user)

    # =====================================
    # Generate OTP
    # =====================================

    otp = generate_email_otp(email)

    # =====================================
    # Send OTP Email
    # =====================================

    html = otp_email(
        username=username,
        otp=otp
    )

    email_sent = send_email(
        recipient=email,
        subject="NovaMind AI - Email Verification Code",
        html=html
    )

    if not email_sent:
        return (
            False,
            "Account created, but the verification email could not be sent."
        )

    # =====================================
    # Success
    # =====================================

    return (
        True,
        "Registration successful! A verification code has been sent to your email."
    )