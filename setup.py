#!/usr/bin/env python3
"""
Jordan OS — Interactive Setup
Walk through entering your real data into jordan.db, step by step.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from data.database import init_db, SessionLocal
from models import Event, FamilyMember, Goal, Milestone, Task, User
from models.event import EventType
from models.family_member import Relationship as FamilyRelationship
from models.goal import GoalCategory, GoalStatus
from models.milestone import MilestoneStatus
from models.task import TaskPriority, TaskStatus
from models.user import UserRole

# ── ANSI ────────────────────────────────────────────────────────────────────

R    = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
RED  = "\033[91m"
GRN  = "\033[92m"
YLW  = "\033[93m"
CYN  = "\033[96m"


def col(text, *codes):
    return "".join(codes) + str(text) + R


# ── Low-level I/O ────────────────────────────────────────────────────────────

def ask(prompt, optional=False, default=None):
    hint = f" [{col(default, DIM)}]" if default is not None else (
        f" {col('(optional)', DIM)}" if optional else ""
    )
    while True:
        val = input(f"  {col('▶', CYN)} {prompt}{hint}: ").strip()
        if not val and default is not None:
            return default
        if not val and optional:
            return None
        if not val:
            print(f"    {col('This field is required.', RED)}")
            continue
        return val


def ask_date(prompt, optional=False):
    hint = f" {col('(optional)', DIM)}" if optional else ""
    while True:
        raw = input(f"  {col('▶', CYN)} {prompt}{hint} [YYYY-MM-DD]: ").strip()
        if not raw and optional:
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print(f"    {col('Use YYYY-MM-DD, e.g. 2026-12-31', RED)}")


def ask_time(prompt, optional=False):
    hint = f" {col('(optional)', DIM)}" if optional else ""
    while True:
        raw = input(f"  {col('▶', CYN)} {prompt}{hint} [HH:MM]: ").strip()
        if not raw and optional:
            return None
        try:
            return datetime.strptime(raw, "%H:%M").time()
        except ValueError:
            print(f"    {col('Use HH:MM, e.g. 09:30', RED)}")


def ask_choice(prompt, choices, default=None):
    opts = "/".join(
        col(ch.upper(), BOLD, CYN) if ch == default else ch
        for ch in choices
    )
    while True:
        raw = input(f"  {col('▶', CYN)} {prompt} [{opts}]: ").strip().lower()
        if not raw and default:
            return default
        if raw in choices:
            return raw
        print(f"    {col('Choose one of: ' + ', '.join(choices), RED)}")


def ask_yn(prompt, default="n"):
    hint = "Y/n" if default == "y" else "y/N"
    raw = input(f"  {col('▶', CYN)} {prompt} [{hint}]: ").strip().lower()
    if not raw:
        return default == "y"
    return raw.startswith("y")


# ── Display helpers ──────────────────────────────────────────────────────────

def blank():
    print()


def ok(msg):
    print(f"  {col('✓', GRN)} {msg}")


def info(msg):
    print(f"    {col(msg, DIM)}")


def warn(msg):
    print(f"  {col('⚠  ' + msg, YLW)}")


def hdr(title, step=None, total=8):
    blank()
    bar = col("─" * 56, CYN)
    print(bar)
    if step:
        print(col(f"  Step {step} of {total}", DIM))
    print(col(f"  {title}", BOLD, CYN))
    print(bar)
    blank()


def sub(title):
    blank()
    print(f"  {col('┌─', DIM)} {col(title, BOLD)}")
    blank()


def banner():
    blank()
    print(col("  ╔══════════════════════════════════════════╗", CYN))
    print(col("  ║          J O R D A N   O S              ║", BOLD, CYN))
    print(col("  ║          Interactive Setup               ║", CYN))
    print(col("  ╚══════════════════════════════════════════╝", CYN))
    blank()
    print(col("  Enter your real data step by step.", DIM))
    print(col("  Everything saves to data/jordan.db", DIM))
    print(col("  Press Ctrl+C at any time to cancel.", DIM))
    blank()


# ── Steps ────────────────────────────────────────────────────────────────────

def step_clear(db):
    hdr("Clear Existing Data", step=1)

    counts = {
        "users":          db.query(User).count(),
        "family_members": db.query(FamilyMember).count(),
        "goals":          db.query(Goal).count(),
        "milestones":     db.query(Milestone).count(),
        "tasks":          db.query(Task).count(),
        "events":         db.query(Event).count(),
    }
    total = sum(counts.values())

    if total == 0:
        ok("Database is empty — nothing to clear.")
        return

    print(col("  Records currently in jordan.db:", BOLD))
    for table, n in counts.items():
        print(f"    {col(table, CYN)}: {n}")
    blank()
    warn(f"This will permanently delete all {total} records.")
    blank()

    if not ask_yn("Clear everything and start fresh?", default="n"):
        blank()
        print(col("  Keeping existing data. New entries will be added alongside it.", YLW))
        blank()
        return

    # Delete in FK-safe order
    db.query(Event).delete()
    db.query(Task).delete()
    db.query(Milestone).delete()
    db.query(Goal).delete()
    db.query(FamilyMember).delete()
    db.query(User).delete()
    db.commit()
    ok("All records deleted.")


def step_profile(db):
    hdr("Your Profile", step=2)
    print(col("  This is the primary account — you.\n", DIM))

    name  = ask("Your name")
    email = ask("Your email")

    user = User(name=name, email=email, role=UserRole.primary)
    db.add(user)
    db.flush()
    ok(f"Profile saved: {col(name, BOLD)} ({email})")
    return user


def step_partner(db, user):
    hdr("Partner Profile", step=3)

    if not ask_yn("Do you have a partner to add?", default="y"):
        info("Skipped.")
        return None

    blank()
    name     = ask("Partner's name")
    email    = ask("Partner's email", optional=True)
    birthday = ask_date("Partner's birthday", optional=True)

    partner_user = User(
        name=name,
        email=email or f"{name.lower().replace(' ', '.')}@example.com",
        role=UserRole.partner,
    )
    db.add(partner_user)
    db.flush()

    fm = FamilyMember(
        user_id=user.id,
        name=name,
        relationship=FamilyRelationship.partner,
        birth_date=birthday,
    )
    db.add(fm)
    db.flush()
    ok(f"Partner saved: {col(name, BOLD)}")
    return fm


def step_kids(db, user):
    hdr("Kids", step=4)

    kids = []
    if not ask_yn("Do you have kids to add?", default="y"):
        info("Skipped.")
        return kids

    while True:
        sub(f"Child {len(kids) + 1}")
        name     = ask("Name")
        birthday = ask_date("Birthday", optional=True)

        fm = FamilyMember(
            user_id=user.id,
            name=name,
            relationship=FamilyRelationship.child,
            birth_date=birthday,
        )
        db.add(fm)
        db.flush()
        kids.append(fm)
        ok(f"Added: {col(name, BOLD)}")

        if not ask_yn("Add another child?", default="n"):
            break

    return kids


_CATEGORIES = [cat.value for cat in GoalCategory]


def step_goals(db, user):
    hdr("Your Goals", step=5)
    print(col("  Big things you're working toward — health, money, family, anything.\n", DIM))

    goals = []
    if not ask_yn("Add a goal?", default="y"):
        info("Skipped.")
        return goals

    while True:
        sub(f"Goal {len(goals) + 1}")
        title       = ask("Title")
        description = ask("Description", optional=True)
        category    = ask_choice("Category", _CATEGORIES, default="personal")
        target_date = ask_date("Target date", optional=True)

        goal = Goal(
            user_id=user.id,
            title=title,
            description=description,
            category=GoalCategory(category),
            status=GoalStatus.active,
            target_date=target_date,
        )
        db.add(goal)
        db.flush()
        goals.append(goal)
        ok(f"Goal saved: {col(title, BOLD)}")

        if not ask_yn("Add another goal?", default="y"):
            break

    return goals


def step_milestones(db, goals):
    hdr("Milestones", step=6)
    print(col("  Break each goal into checkpoints.\n", DIM))

    if not goals:
        info("No goals to attach milestones to. Skipped.")
        return []

    all_milestones = []
    for goal in goals:
        blank()
        print(f"  {col('Goal:', BOLD)} {goal.title}")

        if not ask_yn("  Add milestones for this goal?", default="y"):
            continue

        while True:
            sub(f"Milestone for '{goal.title}'")
            title    = ask("Title")
            due_date = ask_date("Due date", optional=True)

            ms = Milestone(
                goal_id=goal.id,
                title=title,
                due_date=due_date,
                status=MilestoneStatus.pending,
            )
            db.add(ms)
            db.flush()
            all_milestones.append(ms)
            ok(f"Milestone saved: {col(title, BOLD)}")

            if not ask_yn("  Add another milestone for this goal?", default="y"):
                break

    return all_milestones


_PRIORITIES = [p.value for p in TaskPriority]


def step_tasks(db, user, goals):
    hdr("Tasks", step=7)
    print(col("  Day-to-day actions. Optionally link each one to a goal.\n", DIM))

    tasks = []
    if not ask_yn("Add a task?", default="y"):
        info("Skipped.")
        return tasks

    goal_map = {str(i + 1): g for i, g in enumerate(goals)}

    while True:
        sub(f"Task {len(tasks) + 1}")
        title = ask("Title")

        goal_id = None
        if goals:
            print(col("  Your goals:", DIM))
            for i, g in enumerate(goals):
                print(f"    {i + 1}.  {g.title}")
            choice = ask("Which goal? (enter number)", optional=True)
            if choice and choice in goal_map:
                goal_id = goal_map[choice].id
            elif choice:
                warn("Goal number not recognised — task saved without a goal link.")

        due_date = ask_date("Due date", optional=True)
        priority = ask_choice("Priority", _PRIORITIES, default="medium")

        task = Task(
            user_id=user.id,
            goal_id=goal_id,
            title=title,
            status=TaskStatus.pending,
            priority=TaskPriority(priority),
            due_date=due_date,
        )
        db.add(task)
        db.flush()
        tasks.append(task)
        ok(f"Task saved: {col(title, BOLD)}")

        if not ask_yn("Add another task?", default="y"):
            break

    return tasks


_EVENT_TYPES = [et.value for et in EventType]


def step_events(db, user, family_members):
    hdr("Family Events", step=8)
    print(col("  Birthdays, anniversaries, appointments, outings…\n", DIM))

    events = []
    if not ask_yn("Add an event?", default="y"):
        info("Skipped.")
        return events

    fm_map = {str(i + 1): fm for i, fm in enumerate(family_members)}

    while True:
        sub(f"Event {len(events) + 1}")
        title      = ask("Title")
        event_type = ask_choice("Type", _EVENT_TYPES, default="other")
        event_date = ask_date("Date")

        all_day = ask_yn("All-day event?", default="y")
        start_time = datetime.combine(event_date, datetime.min.time())
        end_time   = None

        if not all_day:
            t = ask_time("Start time")
            start_time = datetime.combine(event_date, t)
            t2 = ask_time("End time", optional=True)
            if t2:
                end_time = datetime.combine(event_date, t2)

        recurring      = ask_yn("Recurs every year?", default="n")
        recurrence_rule = "FREQ=YEARLY" if recurring else None

        involved_ids = []
        if family_members:
            blank()
            print(col("  Family members:", DIM))
            for i, fm in enumerate(family_members):
                print(f"    {i + 1}.  {fm.name}")
            raw = input(
                f"  {col('▶', CYN)} Who's involved? "
                f"(comma-separated numbers, {col('Enter to skip', DIM)}): "
            ).strip()
            if raw:
                for part in raw.split(","):
                    key = part.strip()
                    if key in fm_map:
                        involved_ids.append(fm_map[key].id)

        event = Event(
            user_id=user.id,
            title=title,
            event_type=EventType(event_type),
            start_time=start_time,
            end_time=end_time,
            all_day=all_day,
            recurring=recurring,
            recurrence_rule=recurrence_rule,
            family_member_ids=involved_ids,
        )
        db.add(event)
        db.flush()
        events.append(event)
        ok(f"Event saved: {col(title, BOLD)}")

        if not ask_yn("Add another event?", default="y"):
            break

    return events


# ── Summary ──────────────────────────────────────────────────────────────────

def _label(text):
    return col(f"{text}:", CYN)


def show_summary(db, user):
    hdr("Summary — Everything in jordan.db")

    # Profile
    print(col("  YOUR PROFILE", BOLD))
    print(f"    {_label('Name')}   {user.name}")
    print(f"    {_label('Email')}  {user.email}")
    blank()

    # Family
    family = db.query(FamilyMember).filter_by(user_id=user.id).all()
    if family:
        print(col("  FAMILY", BOLD))
        for fm in family:
            dob = str(fm.birth_date) if fm.birth_date else "—"
            print(f"    {col(fm.name, BOLD):<20}  {fm.relationship}   born {dob}")
        blank()

    # Goals + milestones
    goals = db.query(Goal).filter_by(user_id=user.id).all()
    if goals:
        print(col("  GOALS & MILESTONES", BOLD))
        for g in goals:
            due = str(g.target_date) if g.target_date else "no target"
            print(f"    {col(g.title, BOLD)}  {col(f'[{g.category}]', DIM)}  due {due}")
            milestones = db.query(Milestone).filter_by(goal_id=g.id).all()
            for ms in milestones:
                ms_due = str(ms.due_date) if ms.due_date else "—"
                print(f"      {col('○', DIM)} {ms.title}  {col(ms_due, DIM)}")
        blank()

    # Tasks
    tasks = db.query(Task).filter_by(user_id=user.id).all()
    if tasks:
        print(col("  TASKS", BOLD))
        for t in tasks:
            prio_col = YLW if t.priority in (TaskPriority.high, TaskPriority.urgent) else DIM
            due = str(t.due_date) if t.due_date else "—"
            print(f"    [{col(t.priority.upper(), prio_col)}]  {t.title}  {col(due, DIM)}")
        blank()

    # Events
    events = db.query(Event).filter_by(user_id=user.id).all()
    if events:
        print(col("  EVENTS", BOLD))
        for e in events:
            date_str = str(e.start_time)[:10]
            recur    = col("  ↻ yearly", GRN) if e.recurring else ""
            print(f"    {col(date_str, CYN)}  {e.title}  {col(f'({e.event_type})', DIM)}{recur}")
        blank()

    # Totals bar
    ms_count = sum(
        db.query(Milestone).filter_by(goal_id=g.id).count() for g in goals
    )
    print(col("  " + "─" * 52, DIM))
    print(
        f"  {col('Saved:', BOLD)}  "
        f"{col(len(family), GRN, BOLD)} family member{'s' if len(family) != 1 else ''}   "
        f"{col(len(goals), GRN, BOLD)} goal{'s' if len(goals) != 1 else ''}   "
        f"{col(ms_count, GRN, BOLD)} milestone{'s' if ms_count != 1 else ''}   "
        f"{col(len(tasks), GRN, BOLD)} task{'s' if len(tasks) != 1 else ''}   "
        f"{col(len(events), GRN, BOLD)} event{'s' if len(events) != 1 else ''}"
    )
    blank()
    print(col("  To verify, run: python -c \"from core import JordanOS; a=JordanOS(); print(a.summary()); a.close()\"", DIM))
    blank()


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    banner()
    init_db()
    db = SessionLocal()

    try:
        step_clear(db)
        user    = step_profile(db)
        step_partner(db, user)
        step_kids(db, user)
        goals   = step_goals(db, user)
        step_milestones(db, goals)
        step_tasks(db, user, goals)

        # Refresh family list so events can reference everyone added so far
        family = db.query(FamilyMember).filter_by(user_id=user.id).all()
        step_events(db, user, family)

        db.commit()
        blank()
        print(col("  ✓ All data committed to jordan.db", GRN, BOLD))
        show_summary(db, user)

    except KeyboardInterrupt:
        blank()
        blank()
        warn("Setup cancelled. Rolling back all changes.")
        db.rollback()
        blank()
        sys.exit(0)
    except Exception as exc:
        blank()
        print(col(f"  ✗ Something went wrong: {exc}", RED))
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
