"""
=========================================
NovaMind AI - Email Verification Service
=========================================
"""

from database.users import (
    get_user_by_verification_token,
    verify_user_email
)


def verify_email_token(token):
    """
    Verify a user's email using the verification token.
    """

    if not token:
        return (
            False,
            "Verification token is missing."
        )

    user = get_user_by_verification_token(token)

    if not user:
        return (
            False,
            "Invalid or expired verification link."
        )

    verify_user_email(token)

    return (
        True,
        "Your email has been verified successfully!"
    )