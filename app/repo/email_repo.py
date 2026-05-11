from extensions import db
from app.models.Email import Email

def get_all_emails() -> list[Email]:
    """Retrieve all email records from the database.
    Returns:
        list: A list of all Email objects in the database.
    """
    return Email.query.all()

def get_email_desc() -> list[Email]:
    """Retrieve all email records from the database, ordered by creation date in descending order.
    Returns:
        list: A list of all Email objects in the database, ordered by creation date (newest first).
    """
    return Email.query.order_by(Email.id.desc()).all()

def get_email_as_page(start: int, limit: int, sort: str = "desc") -> list[Email]:
    """Retrieve a paginated list of email records from the database.
    Args:
        start (int): The starting index for pagination.
        limit (int): The maximum number of email records to retrieve.
    Returns:
        list: A list of Email objects for the specified page.
    """
    if sort == "desc":
        return Email.query.order_by(Email.id.desc()).offset(start).limit(limit).all()
    else:
        return Email.query.order_by(Email.id.asc()).offset(start).limit(limit).all()

def get_email_by_id(email_id) -> Email | None:
    """Retrieve an email record by its ID.
    Args:
        email_id (int): The ID of the email to retrieve.
    Returns:
        Email: The Email object with the specified ID, or None if not found.
    """
    return Email.query.get(email_id)

def get_email_by_recipient(recipient) -> list[Email]:
    """Retrieve email records by recipient email address.
    Args:
        recipient (str): The email recipient to search for.
    Returns:
        list: A list of Email objects that match the specified recipient.
    """
    return Email.query.filter_by(recipient=recipient).all()

def create_email(recipient, subject, mail_type, body, pdf_path=None) -> Email:
    """Create a new email record in the database.
    Args:
        recipient (str): The email recipient.
        subject (str): The email subject.
        body (str): The email body.
        pdf_path (str): The file path to the generated PDF.
    Returns:
        Email: The created Email object.
    """
    new_email = Email(
        recipient=recipient,
        subject=subject,
        mail_type=mail_type,
        body=body,
        pdf_path=pdf_path
    )
    db.session.add(new_email)
    db.session.commit()
    return new_email

def delete_email(email_id) -> bool:
    """Delete an email record by its ID.
    Args:
        email_id (int): The ID of the email to delete.
    Returns:
        bool: True if the email was deleted, False if not found.
    """
    email = Email.query.get(email_id)
    if email:
        db.session.delete(email)
        db.session.commit()
        return True
    return False