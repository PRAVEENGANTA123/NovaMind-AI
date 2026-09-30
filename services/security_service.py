"""
=========================================
NovaMind AI - Security Service
=========================================
"""

from authentication.password import (
    hash_password,
    verify_password,
)

from database.users import (
    get_user_by_email,
    change_user_password,
)


def update_password(
    email,
    current_password,
    new_password,
    confirm_password,
):

    user = get_user_by_email(email)

    if not user:
        return False, "User not found."

    if not verify_password(
        current_password,
        user["password"],
    ):
        return False, "Current password is incorrect."

    if len(new_password) < 8:
        return False, "Password must contain at least 8 characters."

    if new_password != confirm_password:
        return False, "Passwords do not match."

    if verify_password(
        new_password,
        user["password"],
    ):
        return False, "New password must be different."

    hashed = hash_password(new_password)

    change_user_password(
        email,
        hashed,
    )

    return True, "Password updated successfully."