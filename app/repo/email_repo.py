from extensions import db
from app.models.Email import Email
from sqlalchemy.sql._elements_constructors import desc

def get_all_emails() -> list[Email]:
    """Retrieve all email records from the database.
    Returns:
        list: A list of all Email objects in the database.
    """
    return db.session.scalars(db.select(Email)).all()

def get_email_desc() -> list[Email]:
    """Retrieve all email records from the database, ordered by creation date in descending order.
    Returns:
        list: A list of all Email objects in the database, ordered by creation date (newest first).
    """
    return db.session.scalars(db.select(Email).order_by(desc(Email.id))).all()

def get_email_as_page(start: int, limit: int, sort: str = "desc") -> list[Email]:
    """Retrieve a paginated list of email records from the database.
    Args:
        start (int): The starting index for pagination.
        limit (int): The maximum number of email records to retrieve.
    Returns:
        list: A list of Email objects for the specified page.
    """
    if sort == "desc":
        return db.session.scalars(db.select(Email).order_by(desc(Email.id)).offset(start).limit(limit)).all()
    else:
        return db.session.scalars(db.select(Email).order_by(Email.id).offset(start).limit(limit)).all()

def get_email_by_id(email_id) -> Email | None:
    """Retrieve an email record by its ID.
    Args:
        email_id (int): The ID of the email to retrieve.
    Returns:
        Email: The Email object with the specified ID, or None if not found.
    """
    return db.session.scalars(db.select(Email).filter_by(id=email_id)).first()

def get_email_by_recipient(recipient) -> list[Email]:
    """Retrieve email records by recipient email address.
    Args:
        recipient (str): The email recipient to search for.
    Returns:
        list: A list of Email objects that match the specified recipient.
    """
    return db.session.scalars(db.select(Email).filter_by(recipient=recipient)).all()

def create_email(recipient, subject, mail_type, body, confimation_pdf_path, driver_pdf_path) -> Email:
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
        confirmation_pdf_path=confimation_pdf_path,
        driver_plan_pdf_path=driver_pdf_path
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
    email = db.session.scalars(db.select(Email).filter_by(id=email_id)).first()
    if email:
        db.session.delete(email)
        db.session.commit()
        return True
    return False