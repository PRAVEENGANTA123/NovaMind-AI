"""
=========================================
NovaMind AI - User Database
=========================================
"""

from datetime import datetime

from database.mongodb import users_collection


# =====================================
# Check Email Exists
# =====================================

def email_exists(email):
    """
    Check whether an email already exists.
    """
    return users_collection.find_one({"email": email}) is not None


# =====================================
# Create User
# =====================================

def create_user(user):
    """
    Insert a new user into MongoDB.
    """
    return users_collection.insert_one(user)


# =====================================
# Get User by Email
# =====================================

def get_user_by_email(email):
    """
    Return user by email.
    """
    return users_collection.find_one({"email": email})


# =====================================
# Update Password
# =====================================

def update_password(email, hashed_password):
    """
    Update password and clear reset tokens.
    """

    return users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "password": hashed_password,
                "reset_token": None,
                "token_expiry": None
            }
        }
    )


# =====================================
# Update Last Login
# =====================================

def update_last_login(email, login_time):
    """
    Save last login time.
    """

    return users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "last_login": login_time
            }
        }
    )


# =====================================
# Check Email Verification Status
# =====================================

def is_email_verified(email):
    """
    Return True if email is verified.
    """

    user = users_collection.find_one(
        {
            "email": email
        }
    )

    if not user:
        return False

    return user.get("email_verified", False)


# =====================================
# Save Email OTP
# =====================================

def save_email_otp(email, otp, expiry):
    """
    Save OTP and expiry.
    """

    return users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "email_otp": otp,
                "email_otp_expiry": expiry
            }
        }
    )


# =====================================
# Verify Email OTP
# =====================================

def verify_email_otp(email, otp):
    """
    Return user if OTP is correct and not expired.
    """

    return users_collection.find_one(
        {
            "email": email,
            "email_otp": otp,
            "email_otp_expiry": {
                "$gt": datetime.utcnow()
            }
        }
    )


# =====================================
# Mark Email Verified
# =====================================

def mark_email_verified(email):
    """
    Mark email as verified and clear OTP.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "email_verified": True,
                "email_otp": None,
                "email_otp_expiry": None
            }
        }
    )
# =====================================
# Get User Profile
# =====================================

def get_user_profile(email):
    """
    Return complete profile of a user.
    """

    return users_collection.find_one(
        {
            "email": email
        },
        {
            "_id": 0,
            "password": 0
        }
    )


# =====================================
# Update User Profile
# =====================================

def update_user_profile(
    email,
    username,
    phone,
    occupation,
    country,
    language,
    bio,
):
    """
    Update user profile information.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {

                "username": username,

                "phone": phone,

                "occupation": occupation,

                "country": country,

                "language": language,

                "bio": bio,

            }
        }
    )


# =====================================
# Update Profile Image
# =====================================

def update_profile_image(
    email,
    image_path
):
    """
    Save profile image path.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "profile_image": image_path
            }
        }
    )


# =====================================
# Remove Profile Image
# =====================================

def remove_profile_image(email):
    """
    Remove profile image.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "profile_image": None
            }
        }
    )
# =====================================
# Change Password
# =====================================

def change_user_password(email, hashed_password):
    """
    Update the user's password.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "password": hashed_password
            }
        }
    )
# =====================================
# Get User Settings
# =====================================

def get_user_settings(email):
    """
    Return all user settings.
    """

    user = users_collection.find_one(
        {"email": email},
        {"settings": 1, "_id": 0}
    )

    if not user:
        return {
            "theme": "auto",
            "accent": "Blue",
            "font_size": "Medium",
            "compact_mode": False,

            "language": "English",

            "default_model": "gemini",
            "temperature": 0.7,
            "conversation_memory": True,
            "max_tokens": 2048,

            "auto_save": True,
            "notifications": True,

            "email_notifications": True,
            "desktop_notifications": True,
            "chat_notifications": True,
            "weekly_report": False,
            "sound_alerts": True,
            "marketing_email": False,

            "two_factor": False,
            "login_alerts": True,
            "session_timeout": 30,
        }

    settings = user.get("settings", {})

    defaults = {
        "theme": "auto",
        "accent": "Blue",
        "font_size": "Medium",
        "compact_mode": False,

        "language": "English",

        "default_model": "gemini",
        "temperature": 0.7,
        "conversation_memory": True,
        "max_tokens": 2048,

        "auto_save": True,
        "notifications": True,

        "email_notifications": True,
        "desktop_notifications": True,
        "chat_notifications": True,
        "weekly_report": False,
        "sound_alerts": True,
        "marketing_email": False,

        "two_factor": False,
        "login_alerts": True,
        "session_timeout": 30,
    }

    defaults.update(settings)

    return defaults
# =====================================
# Update User Settings
# =====================================

def update_user_settings(email, settings):
    """
    Save user settings to MongoDB.
    """

    return users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "settings": settings
            }
        }
    )