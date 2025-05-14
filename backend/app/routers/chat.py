from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.schemas.chat_schemas import ChatRequestCreate, ChatRequestResponse, ChatRequestStatusUpdate, ChatRequestHistoryItem
from app.models.user_models import User
from app.models.chat_models import ChatRequest

router = APIRouter()

@router.post("/chat/request", response_model=ChatRequestResponse)
def send_chat_request(
    chat_req: ChatRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_request = ChatRequest(
        sender_node=current_user.node_address,
        receiver_node=chat_req.receiver_node,
        message=chat_req.message,
        status="pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


@router.get("/chat/requests", response_model=list[ChatRequestResponse])
def get_my_chat_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = db.query(ChatRequest).filter(ChatRequest.receiver_node == current_user.node_address).all()
    return requests


@router.patch("/chat/request/{request_id}", response_model=ChatRequestResponse)
def update_chat_request_status(
    request_id: int,
    status_update: ChatRequestStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_req = db.query(ChatRequest).filter(
        ChatRequest.id == request_id,
        ChatRequest.receiver_node == current_user.node_address
    ).first()

    if not chat_req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat request not found")

    chat_req.status = status_update.status
    db.commit()
    db.refresh(chat_req)
    return chat_req



@router.get("/chat/requests/history", response_model=list[ChatRequestHistoryItem])
def get_chat_request_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_requests = db.query(ChatRequest).filter(
        (ChatRequest.sender_node == current_user.node_address) |
        (ChatRequest.receiver_node == current_user.node_address)
    ).all()

    history = []

    for req in all_requests:
        if req.sender_node == current_user.node_address:
            history.append(ChatRequestHistoryItem(
                address=req.receiver_node,
                type="send",
                status=req.status
            ))
        else:
            history.append(ChatRequestHistoryItem(
                address=req.sender_node,
                type="receive",
                status=req.status
            ))

    return history
