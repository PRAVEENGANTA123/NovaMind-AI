from authentication.login import login_user

success, user = login_user(
    "praveen@gmail.com",
    "Password@123"
)

print(success)
print(user)