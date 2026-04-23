from app.service.log_service import service_create_log

def log_system_event(log_type, status:bool):
    """Helper function to log system events.
    Args:
        log_type (str): The type of log entry (e.g., 'email_sent', 'pdf_generated').
        status (bool): The status of the operation (True for success, False for failure).
    """
    user = 'system'
    service_create_log(user, log_type, status)
    
def log_user_event(user, log_type, status:bool):
    """Helper function to log user events.
    Args:
        user (str): The user associated with the log entry.
        log_type (str): The type of log entry (e.g., 'email_sent', 'pdf_generated').
        status (bool): The status of the operation (True for success, False for failure).
    """
    service_create_log(user, log_type, status)