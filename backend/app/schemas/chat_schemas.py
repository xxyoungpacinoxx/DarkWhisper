from pydantic import BaseModel
from typing import Literal

class ChatRequestCreate(BaseModel):
    receiver_node: str
    message: str

class ChatRequestResponse(BaseModel):
    id: int
    sender_node: str
    receiver_node: str
    message: str
    status: Literal["pending", "accepted", "rejected"]

    class Config:
        orm_mode = True

class ChatRequestStatusUpdate(BaseModel):
    status: Literal["accepted", "rejected"]


class ChatRequestHistoryItem(BaseModel):
    address: str  # The other user's node address
    type: str     # "send" or "receive"
    status: str

    class Config:
        orm_mode = True

