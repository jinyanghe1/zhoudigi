from typing import Optional

from fastapi import Header, Query


def get_user_id(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    user_id: Optional[str] = Query(None),
) -> str:
    """Resolve a stable client identifier from header first, then query."""
    return (x_user_id or user_id or "anonymous").strip() or "anonymous"
