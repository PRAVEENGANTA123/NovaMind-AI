"""
=========================================
NovaMind AI - Secure Token Generator
=========================================
"""

import secrets


# =====================================
# Email Verification Token
# =====================================

def generate_verification_token():
    """
    Generate a secure email verification token.
    """
    return secrets.token_urlsafe(32)


# =====================================
# Password Reset Token
# =====================================

def generate_reset_token():
    """
    Generate a secure password reset token.
    """
    return secrets.token_urlsafe(32)


# =====================================
# OTP Generator
# =====================================

def generate_otp():
    """
    Generate a 6-digit OTP.
    """
    return str(secrets.randbelow(900000) + 100000)