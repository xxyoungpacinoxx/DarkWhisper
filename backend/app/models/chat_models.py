from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class ChatRequest(Base):
    __tablename__ = "chat_requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_node = Column(String(512), nullable=False)
    receiver_node = Column(String(512), nullable=False)
    message = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")  # Values: pending, accepted, rejected

    def __repr__(self):
        return f"<ChatRequest(sender={self.sender_node}, receiver={self.receiver_node}, status={self.status})>"
