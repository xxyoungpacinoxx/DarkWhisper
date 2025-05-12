from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, unique=True)
    hashed_password = Column(String(255))
    node_address = Column(String(512), unique=True, index=True)
    
    def __repr__(self):
        return f"<User(username={self.username}, node_address={self.node_address})>"
