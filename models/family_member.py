import enum
from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship
from .base import Base


class Relationship(str, enum.Enum):
    partner = "partner"
    child = "child"
    parent = "parent"
    sibling = "sibling"
    other = "other"


class FamilyMember(Base):
    __tablename__ = "family_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    relationship: Mapped[Relationship] = mapped_column(Enum(Relationship), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = orm_relationship("User", back_populates="family_members")  # noqa: F821

    def __repr__(self) -> str:
        return f"<FamilyMember id={self.id} name={self.name!r} relationship={self.relationship}>"
