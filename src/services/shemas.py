from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserShema(BaseModel):
    tg_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    create_at: Optional[datetime] = None
    