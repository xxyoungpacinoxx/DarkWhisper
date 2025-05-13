from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate, UserLogin, Token
from ..utils import get_password_hash, verify_password, create_access_token
from ..utils import generate_node_address
from app.dependencies import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = get_password_hash(user.password)
    node_address = generate_node_address()
    new_user = User(username=user.username, hashed_password=hashed_pw, node_address=node_address)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully. Please log in."}



@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # prevents JavaScript access
        secure=False,    # only sent via HTTPS
        samesite="Lax", # restricts cross-site cookie sending
        max_age=3600    # 1 hour
    )
    return response


@router.get("/me")
def read_user_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "node_address": current_user.node_address
    }

