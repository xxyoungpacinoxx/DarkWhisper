from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict
from app.schemas.chat_schemas import ChatRequest, ChatResponse

router = APIRouter()

# In-memory active users and sessions
active_connections: Dict[str, WebSocket] = {}
pending_requests: Dict[str, str] = {}

@router.post("/chat/request", response_model=ChatResponse)
async def request_chat(request: ChatRequest):
    if request.receiver_node not in active_connections:
        raise HTTPException(status_code=404, detail="Receiver not connected")

    pending_requests[request.receiver_node] = request.sender_node
    return {"status": "pending", "message": "Request sent"}

@router.post("/chat/accept", response_model=ChatResponse)
async def accept_chat(request: ChatRequest):
    if pending_requests.get(request.receiver_node) != request.sender_node:
        raise HTTPException(status_code=400, detail="No pending request from sender")

    return {"status": "accepted", "message": "Chat accepted"}

@router.websocket("/ws/{node_address}")
async def websocket_endpoint(websocket: WebSocket, node_address: str):
    await websocket.accept()
    active_connections[node_address] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            for target_node, ws in active_connections.items():
                if target_node != node_address:
                    await ws.send_text(f"[{node_address}]: {data}")
    except WebSocketDisconnect:
        del active_connections[node_address]
