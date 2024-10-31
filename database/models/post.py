from dataclasses import dataclass
from datetime import datetime

@dataclass
class PostData:
    post_id: int
    create_date: datetime
    title: str
    body_id: int
    category_id: int
    category: str
    summary: str | None = None
    body: str | None = None
