from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime, Boolean
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            completed_at=self.completed_at,
            is_complete=self.is_complete,
        )

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=None,
            is_complete=False,
        )

    def create_response(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
        }
