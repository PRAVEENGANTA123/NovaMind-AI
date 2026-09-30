from authentication.otp_service import generate_email_otp

otp = generate_email_otp(
    "YOUR_EMAIL@gmail.com"
)

print("OTP:", otp)