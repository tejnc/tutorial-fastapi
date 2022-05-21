from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# declaring base class
Base = declarative_base()

# creating session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)