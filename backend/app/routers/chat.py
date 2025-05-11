from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.dependencies import get_current_user
from app.models.user import User
from jose import JWTError, jwt
from app.utils import SECRET_KEY, ALGORITHM

router = APIRouter()

# In-memory active users and sessions
active_connections: Dict[str, WebSocket] = {}
pending_requests: Dict[str, str] = {}

@router.post("/chat/request", response_model=ChatResponse)
async def request_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if request.receiver_node not in active_connections:
        raise HTTPException(status_code=404, detail="Receiver not connected")

    pending_requests[request.receiver_node] = request.sender_node
    return {"status": "pending", "message": "Request sent"}

@router.post("/chat/accept", response_model=ChatResponse)
async def accept_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if pending_requests.get(request.receiver_node) != request.sender_node:
        raise HTTPException(status_code=400, detail="No pending request from sender")

    return {"status": "accepted", "message": "Chat accepted"}

@router.websocket("/ws/{node_address}")
async def websocket_endpoint(websocket: WebSocket, node_address: str, token: str):
    # Extract and verify token manually for WebSocket
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

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
