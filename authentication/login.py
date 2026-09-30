"""
=========================================
NovaMind AI - User Login Service
=========================================
"""

from datetime import datetime, timezone

from authentication.password import verify_password

from database.users import (
    get_user_by_email,
    update_last_login,
)


# =====================================
# Login User
# =====================================

def login_user(email, password):
    """
    Authenticate a user.

    Returns:
        (True, user)
        (False, message)
    """

    # =====================================
    # Clean Input
    # =====================================

    email = email.strip().lower()

    # =====================================
    # Validation
    # =====================================

    if not email:
        return False, "Please enter your email."

    if not password:
        return False, "Please enter your password."

    # =====================================
    # Find User
    # =====================================

    user = get_user_by_email(email)

    if not user:
        return False, "No account found with this email."

    # =====================================
    # Account Status
    # =====================================

    if not user.get("is_active", True):
        return False, "Your account has been disabled."

    # =====================================
    # Email Verification
    # =====================================

    if not user.get("email_verified", False):
        return (
            False,
            "Please verify your email before logging in."
        )

    # =====================================
    # Password Verification
    # =====================================

    if not verify_password(password, user["password"]):
        return False, "Incorrect password."

    # =====================================
    # Update Last Login
    # =====================================

    update_last_login(
        email=email,
        login_time=datetime.now(timezone.utc)
    )

    # =====================================
    # Success
    # =====================================

    return True, user