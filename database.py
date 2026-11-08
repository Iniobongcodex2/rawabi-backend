from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a database file named "rawabi.db" in your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./rawabi.db"

# The engine is the actual connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is what we use to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what we use to create our database tables
Base = declarative_base()