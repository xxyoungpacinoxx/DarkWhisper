from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:MySecure%40123@localhost:3306/darkwhisper")

# Set up the SQLAlchemy database engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    try:
        # Create all tables defined in the models
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
