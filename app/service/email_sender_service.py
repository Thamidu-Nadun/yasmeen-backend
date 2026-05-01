from .email_service import get_email_by_id
from app.utils.email_sender import send_email_with_attachment
from app.service.log_service import service_create_log

def send_mail_to_recipient(email_id):
    email = get_email_by_id(email_id)
    if email is None:
        print(f"Email with ID {email_id} not found.")
        return False
    recipient = email.recipient
    subject = email.subject
    body = email.body
    attachment = email.pdf_path
    headers = {
        'X-TYPE': email.mail_type,
        'X-COMPANY': "Thamidu Nadun",
    }
    
    if not attachment:
        print(f"No attachment found for email ID {email_id}.")
        return False
    
    if send_email_with_attachment(recipient, subject, body, attachment, headers=headers):
        service_create_log(user="system", log_type=f"Email Sent To: {recipient}", status=True)
        return True
    else:
        service_create_log(user="email@system", log_type="Email Sent", status=False)
        return False