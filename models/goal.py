import enum
from datetime import date, datetime
from sqlalchemy import String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class GoalCategory(str, enum.Enum):
    health = "health"
    finance = "finance"
    career = "career"
    relationships = "relationships"
    personal = "personal"
    education = "education"
    home = "home"


class GoalStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    paused = "paused"
    archived = "archived"


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[GoalCategory] = mapped_column(Enum(GoalCategory), nullable=False)
    status: Mapped[GoalStatus] = mapped_column(Enum(GoalStatus), default=GoalStatus.active)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="goals")  # noqa: F821
    milestones: Mapped[list["Milestone"]] = relationship(  # noqa: F821
        "Milestone", back_populates="goal", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task", back_populates="goal"
    )

    def __repr__(self) -> str:
        return f"<Goal id={self.id} title={self.title!r} status={self.status}>"
