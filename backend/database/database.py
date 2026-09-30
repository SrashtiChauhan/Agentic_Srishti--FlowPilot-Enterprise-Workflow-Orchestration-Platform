import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from backend.database.base import Base 
load_dotenv("backend/.env")


DATABASE_URL=os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

engine = create_engine(
    DATABASE_URL,
)

from backend.database.models.workflow import WorkflowDB
Base.metadata.create_all(bind=engine)
 