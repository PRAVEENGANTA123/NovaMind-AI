"""
=========================================
NovaMind AI - Profile Service
=========================================
"""

from pathlib import Path
import shutil

from database.users import (
    get_user_profile,
    update_user_profile,
    update_profile_image,
)

UPLOAD_FOLDER = Path("uploads/profile_images")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# Get Profile
# ==========================================

def load_profile(email):
    """
    Load user profile from MongoDB.
    """

    return get_user_profile(email)


# ==========================================
# Save Profile
# ==========================================

def save_profile(
    email,
    username,
    phone,
    occupation,
    country,
    language,
    bio,
):
    """
    Save profile details.
    """

    username = username.strip()
    phone = phone.strip()
    occupation = occupation.strip()
    country = country.strip()
    language = language.strip()
    bio = bio.strip()

    # --------------------------
    # Validation
    # --------------------------

    if not username:
        return False, "Full name is required."

    if len(username) < 3:
        return False, "Username is too short."

    if phone:

        if not phone.isdigit():

            return False, "Phone number must contain only digits."

        if len(phone) < 10:

            return False, "Phone number is invalid."

    if len(bio) > 250:

        return False, "Bio should not exceed 250 characters."

    update_user_profile(
        email=email,
        username=username,
        phone=phone,
        occupation=occupation,
        country=country,
        language=language,
        bio=bio,
    )

    return True, "Profile updated successfully."


# ==========================================
# Upload Profile Image
# ==========================================

def save_profile_image(email, uploaded_file):
    """
    Save uploaded profile image.
    """

    if uploaded_file is None:
        return False, "Please select an image."

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension not in ["jpg", "jpeg", "png", "webp"]:
        return False, "Unsupported image format."

    filename = f"{email.replace('@','_').replace('.','_')}.{extension}"

    filepath = UPLOAD_FOLDER / filename

    with open(filepath, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    update_profile_image(
        email=email,
        image_path=str(filepath)
    )

    return True, str(filepath)