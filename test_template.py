from authentication.email_templates import verification_email

html = verification_email(

    "Praveen",

    "http://localhost:8501/verify?token=123456"

)

with open("email_preview.html","w",encoding="utf-8") as f:

    f.write(html)

print("Done")