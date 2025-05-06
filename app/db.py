# #database connection
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# 1) Load variables from .env (must be before you access os.getenv)
load_dotenv()

# 2) Read DATABASE_URL from env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")

# 3) Create the SQLAlchemy engine as before
engine: Engine = create_engine(DATABASE_URL, future=True)
