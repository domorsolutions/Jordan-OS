import enum
from datetime import datetime
from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class UserRole(str, enum.Enum):
    primary = "primary"
    partner = "partner"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.primary)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    goals: Mapped[list["Goal"]] = relationship("Goal", back_populates="user")  # noqa: F821
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")  # noqa: F821
    events: Mapped[list["Event"]] = relationship("Event", back_populates="user")  # noqa: F821
    family_members: Mapped[list["FamilyMember"]] = relationship(  # noqa: F821
        "FamilyMember", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} role={self.role}>"
