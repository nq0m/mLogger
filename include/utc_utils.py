from datetime import datetime, timezone

def now_utc():
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)

def utc_isoformat(dt=None):
    """Return an ISO 8601 string in UTC (with 'Z' suffix)."""
    if dt is None:
        dt = now_utc()
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def utc_ymd(dt=None):
    """Return YYYYMMDD string in UTC."""
    if dt is None:
        dt = now_utc()
    return dt.astimezone(timezone.utc).strftime('%Y%m%d')

def ensure_utc(dt):
    """Ensure a datetime is timezone-aware and in UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
