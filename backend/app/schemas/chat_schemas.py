from pydantic import BaseModel

class ChatRequest(BaseModel):
    sender_node: str
    receiver_node: str

class ChatResponse(BaseModel):
    status: str
    message: str
