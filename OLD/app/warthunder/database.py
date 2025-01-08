from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
import json
from sqlalchemy import func, or_
from datetime import datetime, timedelta
import json

Base = declarative_base()

with open('../db_config.json', 'r') as f:
            config = json.load(f)

DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

engine = create_engine(
    DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
