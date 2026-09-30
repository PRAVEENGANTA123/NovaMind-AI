"""
=========================================
NovaMind AI - Email Templates
=========================================
"""


# ==========================================
# Verification Email
# ==========================================

def verification_email(username, verification_link):

    return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

</head>

<body style="margin:0;padding:40px;background:#F8FAFC;font-family:Arial,sans-serif;">

<div style="
max-width:650px;
margin:auto;
background:#FFFFFF;
border-radius:16px;
padding:40px;
box-shadow:0 10px 30px rgba(0,0,0,.08);
">

<h1 style="
color:#2563EB;
text-align:center;
">

NovaMind AI

</h1>

<h2 style="
text-align:center;
color:#0F172A;
">

Welcome {username}! 👋

</h2>

<p style="
font-size:16px;
color:#475569;
line-height:1.8;
">

Thank you for creating your NovaMind AI account.

Please verify your email address to activate your account.

</p>

<div style="text-align:center;margin:40px 0;">

<a
href="{verification_link}"
style="
background:#2563EB;
color:white;
padding:16px 32px;
text-decoration:none;
border-radius:10px;
font-weight:bold;
display:inline-block;
">

Verify Email

</a>

</div>

<p>

Or copy this link into your browser:

</p>

<p style="word-break:break-all;">

{verification_link}

</p>

<hr>

<p style="
font-size:13px;
color:#64748B;
text-align:center;
">

NovaMind AI v2.0

<br>

Powered by Gemini AI

</p>

</div>

</body>

</html>
"""
# ==========================================
# OTP Verification Email
# ==========================================

def otp_email(username, otp):

    return f"""
<!DOCTYPE html>

<html>

<head>
<meta charset="UTF-8">
<title>NovaMind AI - Email Verification</title>
</head>

<body style="
margin:0;
padding:40px;
background:#F4F7FC;
font-family:Arial,Helvetica,sans-serif;
">

<div style="
max-width:650px;
margin:auto;
background:#ffffff;
border-radius:18px;
padding:45px;
box-shadow:0 10px 30px rgba(0,0,0,.08);
">

<div style="text-align:center;">

<h1 style="
color:#2563EB;
margin-bottom:10px;
font-size:38px;
">
NovaMind AI
</h1>

<h2 style="
color:#0F172A;
margin-bottom:20px;
">
Welcome {username}! 👋
</h2>

</div>

<p style="
font-size:17px;
color:#475569;
line-height:1.8;
text-align:center;
">

Thank you for creating your <b>NovaMind AI</b> account.

<br><br>

To keep your account secure, please verify your email address using the verification code below.

</p>

<div style="
margin:45px 0;
text-align:center;
">

<div style="
display:inline-block;
background:#2563EB;
color:#ffffff;
padding:22px 45px;
border-radius:14px;
font-size:38px;
font-weight:bold;
letter-spacing:12px;
">

{otp}

</div>

</div>

<p style="
text-align:center;
font-size:16px;
color:#475569;
line-height:1.8;
">

This verification code will expire in
<b>10 minutes</b>.

<br><br>

If you didn't create a NovaMind AI account, you can safely ignore this email.

</p>

<hr style="
margin:40px 0;
border:none;
border-top:1px solid #E2E8F0;
">

<p style="
text-align:center;
font-size:13px;
color:#94A3B8;
line-height:1.8;
">

Powered by Gemini AI

<br>

NovaMind AI v2.0 © 2026

</p>

</div>

</body>

</html>
"""

# ==========================================
# Password Reset OTP Email
# ==========================================

def password_reset_email(username, otp):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>NovaMind AI - Password Reset Code</title>
</head>
<body style="margin:0;padding:40px;background:#F4F7FC;font-family:Arial,Helvetica,sans-serif;">
<div style="max-width:650px;margin:auto;background:#ffffff;border-radius:18px;padding:45px;box-shadow:0 10px 30px rgba(0,0,0,.08);">
<div style="text-align:center;">
<h1 style="color:#2563EB;margin-bottom:10px;font-size:38px;">NovaMind AI</h1>
<h2 style="color:#0F172A;margin-bottom:20px;">Password Reset Request 🔐</h2>
</div>
<p style="font-size:17px;color:#475569;line-height:1.8;text-align:center;">
Hello <b>{username}</b>,<br><br>
We received a request to reset your NovaMind AI account password. Use the verification code below to set a new password.
</p>
<div style="margin:45px 0;text-align:center;">
<div style="display:inline-block;background:#DC2626;color:#ffffff;padding:22px 45px;border-radius:14px;font-size:38px;font-weight:bold;letter-spacing:12px;">
{otp}
</div>
</div>
<p style="text-align:center;font-size:16px;color:#475569;line-height:1.8;">
This verification code will expire in <b>10 minutes</b>.<br><br>
If you did not request a password reset, please ignore this email or contact support if you suspect unauthorized activity.
</p>
<hr style="margin:40px 0;border:none;border-top:1px solid #E2E8F0;">
<p style="text-align:center;font-size:13px;color:#94A3B8;line-height:1.8;">
Powered by Gemini AI • NovaMind AI v2.0 © 2026
</p>
</div>
</body>
</html>
"""
