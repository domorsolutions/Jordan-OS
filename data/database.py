import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

_DATA_DIR = Path(__file__).parent
DB_PATH = os.getenv("DATABASE_URL", f"sqlite:///{_DATA_DIR}/jordan.db")

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models import Base
    Base.metadata.create_all(bind=engine)
    print(f"Database initialised at: {DB_PATH}")
