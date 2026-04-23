import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST") or "smtp.gmail.com"
SMTP_PORT = int(os.getenv("SMTP_PORT") or 587)

EMAIL_ADDR = os.getenv("SMTP_MAIL") or "test@gmail.com"
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD") or "password"

def send_email(to_email: str, subject: str, body: str):
    """Send email with the specified subject and body to the given email address

    Args:
        to_email (string): the recipient email address
        subject (string): the subject of the email
        body (TEXT): the body content of the email
    """
    msg = MIMEText(body)
    msg['From'] = EMAIL_ADDR
    msg['To'] = to_email
    msg['Subject'] = subject
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDR, EMAIL_PASSWORD)
        
        server.sendmail(EMAIL_ADDR, to_email, msg.as_string())
        
        print(f"Email sent to {to_email} with subject '{subject}'")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
        
def send_email_with_attachment(to_email, subject, body, attachment_path):
    """Send email with an attachment

    Args:
        to_email (string): email address of the recipient
        subject (string): email subject
        body (string): email body content
        attachment_path (string): path to the file to be attached
    Returns:
        bool: True -> email sent successfully, False -> failed to send email
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDR
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDR, EMAIL_PASSWORD)
        
        server.sendmail(EMAIL_ADDR, to_email, msg.as_string())
        
        print(f"Email with attachment sent to {to_email} with subject '{subject}'")
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email with attachment: {e}")
        return False
        