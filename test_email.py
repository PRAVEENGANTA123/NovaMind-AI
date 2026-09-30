from authentication.email_service import send_email

html = """

<h1>Hello Praveen 👋</h1>

<p>

NovaMind AI Email Service Working Successfully.

</p>

"""

success = send_email(

    "YOUR_EMAIL@gmail.com",

    "NovaMind AI Test",

    html

)

print(success)
