from authentication.register import Register

success, message = Register.create(

    "Praveen",

    "praveen@gmail.com",

    "Password@123"

)

print(success)

print(message)