# app/models.py
import datetime
from typing import Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles ORM."""

    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    due_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, nullable=True
    )
    status: Mapped[str] = mapped_column(String, nullable=False)

    def to_dict(self) -> dict:
        """
        Convertit l'instance de Task en dictionnaire pour la sérialisation JSON.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
        }

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title}>"
