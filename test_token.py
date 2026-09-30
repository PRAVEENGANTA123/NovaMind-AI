from utils.token import (
    generate_verification_token,
    generate_reset_token,
    generate_otp
)

print("Verification Token:")
print(generate_verification_token())

print()

print("Reset Token:")
print(generate_reset_token())

print()

print("OTP:")
print(generate_otp())