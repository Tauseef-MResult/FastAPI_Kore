import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email(email: str, name: str, password: str):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_USER")
    msg['To'] = email
    msg['Subject'] = "Your Account Password for Idea Submission Chatbot"

    body = f"""
    <p>Dear {name},</p>
    <p>Your account has been created successfully.</p>
    <p>Your password is: <strong>{password}</strong></p>
    <p>Thank you!</p>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASS"))
        server.sendmail(os.getenv("MAIL_USER"), email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False