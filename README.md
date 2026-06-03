# Jordan OS
> A personal life operating system — like Jarvis, but yours.

Jordan OS is a Python-based, AI-augmented system for managing goals, tasks, family life, and everything in between. It starts with a clean data layer and grows into an intelligent personal assistant.

---

## 6-Phase Build Plan

### Phase 1 — Foundation (current)
**Data layer, schemas, family unit, seed data**
- SQLite database (`data/jordan.db`) via SQLAlchemy ORM
- Models: `users`, `goals`, `milestones`, `tasks`, `family_members`, `events`
- Family unit: primary user + partner + kids
- Seed script with realistic sample data
- `.env.example` with placeholder config

### Phase 2 — Core Logic
**Goal tracking, task management, family dashboard**
- CRUD operations for all entities via a clean service layer
- Goal progress calculation (milestone completion %)
- Task prioritisation and due-date engine
- Family event calendar aggregation
- CLI interface to query and update data

### Phase 3 — AI Integration
**Natural language queries and smart suggestions (OpenAI)**
- Wire up `OPENAI_API_KEY`
- Natural language interface: "What should I focus on today?"
- AI-generated weekly review summaries
- Smart task decomposition from goals
- Conversational goal check-ins

### Phase 4 — Notifications & Reminders
**Proactive nudges so nothing slips**
- Email digests (daily / weekly)
- Birthday and anniversary reminders
- Overdue task alerts
- Optional calendar sync (Google / iCal export)

### Phase 5 — Web UI
**Browser dashboard for the whole family**
- Flask or FastAPI backend exposing a REST API
- React frontend with goal progress cards, task board, family calendar
- Mobile-friendly layout
- Auth for primary user and partner

### Phase 6 — Advanced Intelligence
**Pattern recognition, life analytics, automation**
- Habit tracking and streak analytics
- Goal success prediction from historical data
- Automated task creation from recurring patterns
- Voice interface (Whisper + TTS)
- "Jordan OS Daily Brief" — morning summary delivered to phone

---

## Project Structure

```
Jordan-OS/
├── core/           # Main application logic (JordanOS class)
├── data/           # Database setup (jordan.db lives here)
├── models/         # SQLAlchemy ORM schemas
│   ├── user.py
│   ├── family_member.py
│   ├── goal.py
│   ├── milestone.py
│   ├── task.py
│   └── event.py
├── seed.py         # Populate the database with sample data
├── .env.example    # Environment variable template
├── requirements.txt
└── README.md
```

---

## Getting Started

```bash
# 1. Clone and create a virtual environment
git clone https://github.com/domorsolutions/jordan-os.git
cd jordan-os
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env as needed (SQLite default works out of the box)

# 4. Initialise and seed the database
python seed.py

# 5. Verify it worked
python - <<'EOF'
from core import JordanOS
os = JordanOS()
print(os.summary())
os.close()
EOF
```

---

## Family Unit (seed data)

| Name   | Role    | Notes                       |
|--------|---------|-----------------------------|
| Jordan | Primary | Goals, tasks, events owner  |
| Morgan | Partner | Separate user account       |
| Alex   | Child   | Born Aug 5 2016             |
| Riley  | Child   | Born Mar 14 2019            |

---

## Contributing / Roadmap
This is a personal project. Phases are built sequentially — each phase's branch will be merged to `main` when complete.
