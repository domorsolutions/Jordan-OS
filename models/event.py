import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class EventType(str, enum.Enum):
    appointment = "appointment"
    birthday = "birthday"
    anniversary = "anniversary"
    reminder = "reminder"
    meeting = "meeting"
    family = "family"
    other = "other"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType), default=EventType.other)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)
    recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_rule: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # JSON list of family_member IDs involved in this event
    family_member_ids: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="events")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Event id={self.id} title={self.title!r} type={self.event_type} start={self.start_time}>"
