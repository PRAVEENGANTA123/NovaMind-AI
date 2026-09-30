"""
=========================================
NovaMind AI - Verify OTP Service
=========================================
"""

from database.users import (
    get_user_by_email,
    verify_email_otp,
    mark_email_verified
)


# =====================================
# Verify OTP
# =====================================

def verify_otp(email, otp):
    """
    Verify user's email OTP.

    Returns:
        (True, message)
        (False, message)
    """

    # =====================================
    # Validation
    # =====================================

    if not email:
        return False, "Email not found."

    if not otp:
        return False, "Please enter the verification code."

    otp = otp.strip()

    if len(otp) != 6 or not otp.isdigit():
        return False, "Please enter a valid 6-digit OTP."

    # =====================================
    # User Exists
    # =====================================

    user = get_user_by_email(email)

    if not user:
        return False, "User not found."

    # =====================================
    # Already Verified
    # =====================================

    if user.get("email_verified", False):
        return True, "Your email is already verified."

    # =====================================
    # Verify OTP
    # =====================================

    verified_user = verify_email_otp(
        email=email,
        otp=otp
    )

    if not verified_user:
        return False, "Invalid or expired OTP."

    # =====================================
    # Mark Verified
    # =====================================

    mark_email_verified(email)

    return True, "🎉 Email verified successfully!"