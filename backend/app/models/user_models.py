from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, unique=True)
    node_address = Column(String(256), unique=True, index=True)
    
    def __repr__(self):
        return f"<User(username={self.username}, node_address={self.node_address})>"
