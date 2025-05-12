from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.routers import chat, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield
    # Shutdown logic (if needed)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Use your actual frontend domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(chat.router)
app.include_router(auth.router)


# Serve static files (JS, CSS, etc. if needed)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Route to serve register HTML
@app.get("/register")
def get_register_page():
    return FileResponse("app/static/register/register.html", media_type='text/html')


# Route to serve login HTML
@app.get("/login")
def get_login_page():
    return FileResponse("app/static/login/login.html", media_type='text/html')


# Route to serve login HTML
@app.get("/dashboard")
def get_login_page():
    return FileResponse("app/static/dashboard/dashboard.html", media_type='text/html')