# DarkWhisper

DarkWhisper is a secure, anonymous, real-time web messaging application. It enables users to chat without revealing their identity. Each user connects via a 256-character anonymous ID. Messages are encrypted, and sessions are temporary and user-controlled.

## Features (Planned)
- Anonymous identity (no username or email)
- Real-time chat using WebSockets
- End-to-end encryption (E2EE)
- Session-based interaction (user must accept connection)
- Easy chat termination with no history
- Fast and lightweight UI

## Tech Stack
- FastAPI (Python)
- WebSockets
- JavaScript frontend (React or Vanilla)
- Optional: AES/WebCrypto for E2EE

## Getting Started
1. Clone the repository
2. Install backend dependencies
3. Run the FastAPI server

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
