from .email_repo import get_all_emails, get_email_by_id, create_email, delete_email
from .LogRepo import get_all_logs, get_log_by_id, create_log, delete_log

__all__ = [
    'get_all_emails',
    'get_email_by_id',
    'create_email',
    'delete_email',
    'get_all_logs',
    'get_log_by_id',
    'create_log',
    'delete_log'
]
