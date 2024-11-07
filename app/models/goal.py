from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
        )

    def create_response(self):
        return {
            "id": self.id,
            "title": self.title,
        }
