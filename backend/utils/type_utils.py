from datetime import datetime, timezone


def to_datetime(ts: int):
    return datetime.fromtimestamp(ts, tz=timezone.utc)
