"""
Seed the database with sample data for the Jordan family unit.
Run: python seed.py
"""

from datetime import date, datetime, timedelta
from data.database import init_db, SessionLocal
from models import User, FamilyMember, Goal, Milestone, Task, Event
from models.user import UserRole
from models.family_member import Relationship
from models.goal import GoalCategory, GoalStatus
from models.milestone import MilestoneStatus
from models.task import TaskPriority, TaskStatus
from models.event import EventType


def seed():
    init_db()
    db = SessionLocal()

    try:
        # ----------------------------------------------------------------
        # Users
        # ----------------------------------------------------------------
        jordan = User(name="Jordan", email="jordan@example.com", role=UserRole.primary)
        morgan = User(name="Morgan", email="morgan@example.com", role=UserRole.partner)
        db.add_all([jordan, morgan])
        db.flush()

        # ----------------------------------------------------------------
        # Family members (linked to primary user)
        # ----------------------------------------------------------------
        partner = FamilyMember(
            user_id=jordan.id,
            name="Morgan",
            relationship=Relationship.partner,
            birth_date=date(1990, 4, 22),
            notes="Partner — synced as separate user account",
        )
        child1 = FamilyMember(
            user_id=jordan.id,
            name="Alex",
            relationship=Relationship.child,
            birth_date=date(2016, 8, 5),
        )
        child2 = FamilyMember(
            user_id=jordan.id,
            name="Riley",
            relationship=Relationship.child,
            birth_date=date(2019, 3, 14),
        )
        db.add_all([partner, child1, child2])
        db.flush()

        # ----------------------------------------------------------------
        # Goals
        # ----------------------------------------------------------------
        goal_fitness = Goal(
            user_id=jordan.id,
            title="Get to 185 lbs and run a 5K",
            description="Lose 20 lbs and complete a 5K race by end of year.",
            category=GoalCategory.health,
            status=GoalStatus.active,
            target_date=date(2026, 12, 31),
        )
        goal_savings = Goal(
            user_id=jordan.id,
            title="Build $25,000 emergency fund",
            description="3-month emergency fund covering all household expenses.",
            category=GoalCategory.finance,
            status=GoalStatus.active,
            target_date=date(2027, 6, 1),
        )
        goal_learning = Goal(
            user_id=jordan.id,
            title="Learn Python and ship Jordan OS",
            description="Complete Jordan OS Phases 1-6 and use it daily.",
            category=GoalCategory.education,
            status=GoalStatus.active,
            target_date=date(2026, 12, 31),
        )
        goal_family = Goal(
            user_id=jordan.id,
            title="One intentional family outing per month",
            description="Plan and execute a meaningful family activity every month.",
            category=GoalCategory.relationships,
            status=GoalStatus.active,
            target_date=date(2026, 12, 31),
        )
        db.add_all([goal_fitness, goal_savings, goal_learning, goal_family])
        db.flush()

        # ----------------------------------------------------------------
        # Milestones
        # ----------------------------------------------------------------
        ms_fitness = [
            Milestone(
                goal_id=goal_fitness.id,
                title="Lose first 5 lbs",
                status=MilestoneStatus.completed,
                due_date=date(2026, 3, 31),
                completed_at=datetime(2026, 3, 28),
            ),
            Milestone(
                goal_id=goal_fitness.id,
                title="Run 1 mile without stopping",
                status=MilestoneStatus.completed,
                due_date=date(2026, 4, 30),
                completed_at=datetime(2026, 4, 15),
            ),
            Milestone(
                goal_id=goal_fitness.id,
                title="Run a 5K race",
                status=MilestoneStatus.in_progress,
                due_date=date(2026, 9, 30),
            ),
            Milestone(
                goal_id=goal_fitness.id,
                title="Reach 185 lbs",
                status=MilestoneStatus.pending,
                due_date=date(2026, 12, 31),
            ),
        ]

        ms_savings = [
            Milestone(
                goal_id=goal_savings.id,
                title="Save first $5,000",
                status=MilestoneStatus.in_progress,
                due_date=date(2026, 9, 1),
            ),
            Milestone(
                goal_id=goal_savings.id,
                title="Reach $15,000",
                status=MilestoneStatus.pending,
                due_date=date(2027, 1, 1),
            ),
            Milestone(
                goal_id=goal_savings.id,
                title="Full $25,000 emergency fund",
                status=MilestoneStatus.pending,
                due_date=date(2027, 6, 1),
            ),
        ]

        ms_learning = [
            Milestone(
                goal_id=goal_learning.id,
                title="Phase 1 — Data layer complete",
                status=MilestoneStatus.in_progress,
                due_date=date(2026, 6, 15),
            ),
            Milestone(
                goal_id=goal_learning.id,
                title="Phase 2 — Core logic complete",
                status=MilestoneStatus.pending,
                due_date=date(2026, 7, 15),
            ),
            Milestone(
                goal_id=goal_learning.id,
                title="Phase 3 — AI integration live",
                status=MilestoneStatus.pending,
                due_date=date(2026, 9, 1),
            ),
        ]

        all_milestones = ms_fitness + ms_savings + ms_learning
        db.add_all(all_milestones)
        db.flush()

        # ----------------------------------------------------------------
        # Tasks
        # ----------------------------------------------------------------
        today = date.today()

        tasks = [
            # Fitness
            Task(
                user_id=jordan.id,
                goal_id=goal_fitness.id,
                milestone_id=ms_fitness[2].id,
                title="Sign up for a local 5K race",
                priority=TaskPriority.high,
                status=TaskStatus.pending,
                due_date=today + timedelta(days=7),
            ),
            Task(
                user_id=jordan.id,
                goal_id=goal_fitness.id,
                title="Complete week 4 of Couch to 5K",
                priority=TaskPriority.medium,
                status=TaskStatus.pending,
                due_date=today + timedelta(days=3),
            ),
            Task(
                user_id=jordan.id,
                goal_id=goal_fitness.id,
                title="Buy proper running shoes",
                priority=TaskPriority.high,
                status=TaskStatus.completed,
                completed_at=datetime.utcnow() - timedelta(days=10),
                due_date=today - timedelta(days=14),
            ),
            # Savings
            Task(
                user_id=jordan.id,
                goal_id=goal_savings.id,
                milestone_id=ms_savings[0].id,
                title="Set up automatic $500/month transfer to savings",
                priority=TaskPriority.urgent,
                status=TaskStatus.pending,
                due_date=today + timedelta(days=2),
            ),
            Task(
                user_id=jordan.id,
                goal_id=goal_savings.id,
                title="Review and cancel unused subscriptions",
                priority=TaskPriority.medium,
                status=TaskStatus.in_progress,
                due_date=today + timedelta(days=14),
            ),
            # Jordan OS
            Task(
                user_id=jordan.id,
                goal_id=goal_learning.id,
                milestone_id=ms_learning[0].id,
                title="Implement Phase 1 data layer",
                priority=TaskPriority.urgent,
                status=TaskStatus.in_progress,
                due_date=today,
            ),
            Task(
                user_id=jordan.id,
                goal_id=goal_learning.id,
                title="Write tests for all models",
                priority=TaskPriority.medium,
                status=TaskStatus.pending,
                due_date=today + timedelta(days=5),
            ),
            # Family
            Task(
                user_id=jordan.id,
                goal_id=goal_family.id,
                title="Plan June family outing — kids pick the activity",
                priority=TaskPriority.medium,
                status=TaskStatus.pending,
                due_date=today + timedelta(days=4),
            ),
        ]
        db.add_all(tasks)
        db.flush()

        # ----------------------------------------------------------------
        # Events
        # ----------------------------------------------------------------
        events = [
            Event(
                user_id=jordan.id,
                title="Alex's Birthday",
                event_type=EventType.birthday,
                start_time=datetime(2026, 8, 5, 0, 0),
                all_day=True,
                recurring=True,
                recurrence_rule="FREQ=YEARLY",
                family_member_ids=[child1.id],
            ),
            Event(
                user_id=jordan.id,
                title="Riley's Birthday",
                event_type=EventType.birthday,
                start_time=datetime(2026, 3, 14, 0, 0),
                all_day=True,
                recurring=True,
                recurrence_rule="FREQ=YEARLY",
                family_member_ids=[child2.id],
            ),
            Event(
                user_id=jordan.id,
                title="Morgan's Birthday",
                event_type=EventType.birthday,
                start_time=datetime(2026, 4, 22, 0, 0),
                all_day=True,
                recurring=True,
                recurrence_rule="FREQ=YEARLY",
                family_member_ids=[partner.id],
            ),
            Event(
                user_id=jordan.id,
                title="Family Movie Night",
                description="Monthly family tradition — kids choose the movie.",
                event_type=EventType.family,
                start_time=datetime.utcnow().replace(day=1) + timedelta(days=14),
                end_time=datetime.utcnow().replace(day=1) + timedelta(days=14, hours=2),
                all_day=False,
                family_member_ids=[partner.id, child1.id, child2.id],
            ),
            Event(
                user_id=jordan.id,
                title="Annual Check-up",
                event_type=EventType.appointment,
                start_time=datetime(2026, 7, 10, 9, 0),
                end_time=datetime(2026, 7, 10, 10, 0),
            ),
            Event(
                user_id=jordan.id,
                title="Jordan & Morgan Anniversary",
                event_type=EventType.anniversary,
                start_time=datetime(2026, 10, 18, 0, 0),
                all_day=True,
                recurring=True,
                recurrence_rule="FREQ=YEARLY",
                family_member_ids=[partner.id],
            ),
        ]
        db.add_all(events)
        db.commit()

        print("Seed complete.")
        print(f"  Users:          {db.query(User).count()}")
        print(f"  Family members: {db.query(FamilyMember).count()}")
        print(f"  Goals:          {db.query(Goal).count()}")
        print(f"  Milestones:     {db.query(Milestone).count()}")
        print(f"  Tasks:          {db.query(Task).count()}")
        print(f"  Events:         {db.query(Event).count()}")

    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


if __name__ == "__main__":
    seed()
