from extensions import db
from app.models.Log import Log


def get_all_logs():
    """Retrieve all log records from the database.
    Returns:
        list: A list of all Log objects in the database.
    """
    return Log.query.all()

def get_log_by_id(log_id):
    """Retrieve a log record by its ID.
    Args:
        log_id (int): The ID of the log to retrieve.
    Returns:
        Log: The Log object with the specified ID, or None if not found.
    """
    return Log.query.get(log_id)

def create_log(user, log_type, timestamp, status):
    """Create a new log record in the database.
    Args:
        user (str): The user associated with the log entry.
        log_type (str): The type of log entry (e.g., 'email_sent', 'pdf_generated').
        timestamp (datetime): The timestamp of the log entry.
        status (bool): The status of the operation (True for success, False for failure).
    Returns:
        Log: The created Log object.
    """
    new_log = Log(
        user=user,
        type=log_type,
        timestamp=timestamp,
        status=status
    )
    db.session.add(new_log)
    db.session.commit()
    return new_log

def delete_log(log_id):
    """Delete a log record by its ID.
    Args:
        log_id (int): The ID of the log to delete.
    Returns:
        bool: True if the log was deleted, False if not found.
    """
    log = Log.query.get(log_id)
    if log:
        db.session.delete(log)
        db.session.commit()
        return True
    return False