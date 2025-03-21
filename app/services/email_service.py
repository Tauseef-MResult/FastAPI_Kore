import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_account_creation_email(email: str, name: str, password: str):
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


def send_idea_submission_email(email: str, name: str, idea_id: str, title: str, category: str):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_USER")
    msg['To'] = email
    msg['Subject'] = "Your Idea Has Been Submitted Successfully"

    body = f"""
    <p>Dear {name},</p>
    <p>Your idea has been submitted successfully. Below are the details of your submission:</p>
    <ul>
        <li><strong>Idea ID:</strong> {idea_id}</li>
        <li><strong>Title:</strong> {title}</li>
        <li><strong>Category:</strong> {category}</li>
    </ul>
    <p>Your idea will now be reviewed by the respective department heads. You will receive further notifications once the review process is complete.</p>
    <p>Thank you for your contribution!</p>
    <p>Best regards,</p>
    <p><strong>Innovation Team</strong></p>
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


def send_evaluation_notification(email: str, name: str, idea_title: str, idea_category: str, status: str, comments: str):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_USER")
    msg['To'] = email
    msg['Subject'] = f"Your Idea '{idea_title}' Has Been {status}"

    body = f"""
    <p>Dear {name},</p>
    <p>Your idea has been evaluated. Below are the details:</p>
    <ul>
        <li><strong>Idea Title:</strong> {idea_title}</li>
        <li><strong>Category:</strong> {idea_category}</li>
        <li><strong>Status:</strong> {status}</li>
        <li><strong>Comments:</strong> {comments}</li>
    </ul>
    <p>Thank you for your contribution!</p>
    <p>Best regards,</p>
    <p><strong>Innovation Team</strong></p>
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