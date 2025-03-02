from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DebuggingHistory(Base):
    __tablename__ = "debugging_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    code = Column(Text)
    errors = Column(Text)
    fixes = Column(Text)
    created_at = Column(TIMESTAMP)