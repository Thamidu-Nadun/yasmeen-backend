import os, time
from app.repo.email_repo import get_all_emails, get_email_by_id, get_email_by_recipient, create_email, delete_email
from app.utils.email_parser import extract_email_data
from app.utils.pdf_generation import save_pdf
from app.utils.logger import log_system_event, log_user_event

def get_emails() -> list[dict]:
    return [email.to_dict() for email in get_all_emails()]

def get_email(email_id) -> dict | None:
    email = get_email_by_id(email_id)
    return email.to_dict() if email else None

def get_email_by_mali(recipient) -> list[dict]:
    emails = get_email_by_recipient(recipient)
    print(f"Emails found for recipient {recipient}: {[email.to_dict() for email in emails]}")
    return [email.to_dict() for email in emails]

def save_email(recipient, subject, body, mail_type) -> dict | None:
    if not recipient or not subject or not body:
        raise ValueError("Recipient, subject, and body are required.")
    
    # 1. extract email data from the body
    try:
        global email_content
        email_content = extract_email_data(body)
        print("parsed email", email_content)
        log_user_event(recipient, f"Email parsed successfully for recipient: {recipient}", True)
    except Exception as e:
        log_system_event(f"Email parsing failed: {recipient}", False)
        raise ValueError(f"Failed to parse email content: {e}")
    
    # 2. generate PDF and save it
    try:
    # 2.1 generate the path
        pdf_path = os.path.join("pdf", time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"))
        print(f"Generated PDF path: {pdf_path}")
    
    # 2.2 save the PDF
        global absolute_pdf_path
        saved_pdf_path = save_pdf(recipient, email_content, pdf_path)
        absolute_pdf_path = os.path.abspath(saved_pdf_path)
        print(f"PDF saved at: {absolute_pdf_path}")
        
        log_user_event(recipient, f"PDF generated and saved successfully at {absolute_pdf_path}", True)
    except Exception as e:
        log_system_event(f"PDF generation failed: {e}", False)
        raise ValueError(f"Failed to generate PDF: {e}")
    
    # 3. save email data to the database
    try:
        saved_mail = create_email(recipient=recipient, 
                    subject=subject, 
                    mail_type=mail_type,
                    body=body, 
                    pdf_path=absolute_pdf_path)
        
        log_user_event(recipient, f"Email saved successfully", True)
        return saved_mail.to_dict() if saved_mail else None
    except Exception as e:
        log_system_event(f"Email saving failed: {e}", False)
        raise ValueError(f"Failed to save email: {e}")
    
def delete_email_by_id(email_id):
    email = get_email_by_id(email_id)
    if not email:
        return False
    log_user_event(email.recipient, f"Email with ID {email_id} deleted", True)
    return delete_email(email_id)