from dotenv import load_dotenv
import os 
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta



load_dotenv()


def send_verification_email(email, code):
    '''Send a verification email with provideed data'''

    sender_email = os.getenv("EMAIL_USER")
    email_code = os.getenv("EMAIL_APP_CODE")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = f'Email verification code: {code}'

    body = f"Your verification code is {code}. It expires in 10 minutes."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, email_code)
            server.send_message(msg)
        print(f"Veriifcation email sent to {email} and code : {code}")
    except Exception as e:
        print(f"Error sending email: {e}")
