from data.database import init_db, SessionLocal
from models import User, FamilyMember, Goal, Milestone, Task, Event


class JordanOS:
    """Entry point for the Jordan OS application."""

    def __init__(self):
        init_db()
        self.db = SessionLocal()

    def close(self):
        self.db.close()

    # ------------------------------------------------------------------
    # User helpers
    # ------------------------------------------------------------------

    def get_primary_user(self) -> User | None:
        from models.user import UserRole
        return self.db.query(User).filter(User.role == UserRole.primary).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    # ------------------------------------------------------------------
    # Goal helpers
    # ------------------------------------------------------------------

    def get_active_goals(self, user_id: int) -> list[Goal]:
        from models.goal import GoalStatus
        return (
            self.db.query(Goal)
            .filter(Goal.user_id == user_id, Goal.status == GoalStatus.active)
            .all()
        )

    # ------------------------------------------------------------------
    # Task helpers
    # ------------------------------------------------------------------

    def get_pending_tasks(self, user_id: int) -> list[Task]:
        from models.task import TaskStatus
        return (
            self.db.query(Task)
            .filter(Task.user_id == user_id, Task.status == TaskStatus.pending)
            .order_by(Task.due_date.asc())
            .all()
        )

    # ------------------------------------------------------------------
    # Family helpers
    # ------------------------------------------------------------------

    def get_family(self, user_id: int) -> list[FamilyMember]:
        return self.db.query(FamilyMember).filter(FamilyMember.user_id == user_id).all()

    # ------------------------------------------------------------------
    # Event helpers
    # ------------------------------------------------------------------

    def get_upcoming_events(self, user_id: int, limit: int = 10) -> list[Event]:
        from datetime import datetime
        return (
            self.db.query(Event)
            .filter(Event.user_id == user_id, Event.start_time >= datetime.utcnow())
            .order_by(Event.start_time.asc())
            .limit(limit)
            .all()
        )

    def summary(self) -> dict:
        user = self.get_primary_user()
        if not user:
            return {"error": "No primary user found. Run seed.py first."}
        return {
            "user": user.name,
            "active_goals": len(self.get_active_goals(user.id)),
            "pending_tasks": len(self.get_pending_tasks(user.id)),
            "family_members": len(self.get_family(user.id)),
            "upcoming_events": len(self.get_upcoming_events(user.id)),
        }
