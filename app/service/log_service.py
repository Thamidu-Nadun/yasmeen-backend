from app.repo.LogRepo import get_all_logs, get_log_by_id, create_log, delete_log
from app.models.Log import Log
from datetime import datetime

def service_get_logs() -> list[Log]:
    return [log.to_dict() for log in get_all_logs()]

def service_get_log(log_id) -> dict | None:
    log = get_log_by_id(log_id)
    return log.to_dict() if log else None

def service_create_log(user:str, log_type:str, status:bool) -> dict | None:
    print(f"Creating log: {user} - {log_type} - {'Success' if status else 'Failure'}")
    timestamp = datetime.now()
    log = create_log(user, log_type, timestamp, status)
    return log.to_dict() if log else None

def service_delete_log(log_id) -> bool:
    return delete_log(log_id)