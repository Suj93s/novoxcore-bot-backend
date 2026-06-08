import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag import answer_question

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
try:
    if MONGO_URI:
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client["chat_logs_db"]
        chat_logs_collection = mongo_db["CoreBotChatLogs"]
except Exception as e:
    print("Failed to connect to MongoDB. Check your credentials and configuration.")


app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://novoxcore.com",
        "https://www.novoxcore.com",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str
    tenant: Optional[str] = None
    session_id: Optional[str] = None


class IndexRequest(BaseModel):
    tenant: str
    url: str


@app.post("/chat")
def chat(query: Query):

    if not query.session_id:
        query.session_id = str(uuid.uuid4())

    answer, sources = answer_question(
        query.question
    )

    try:
        chat_logs_collection.insert_one({
            "session_id": query.session_id,
            "question": query.question,
            "answer": answer,
            "timestamp": datetime.now(timezone.utc),
            "sources": sources
        })
    except Exception as e:
        print(f"Failed to log chat to MongoDB: {e}")

    return {
        "answer": answer,
        "session_id": query.session_id
    }


@app.post("/index-website")
def index_website(req: IndexRequest):
    return {"chunks_stored": 10}


@app.delete("/end-chat/{session_id}")
def end_chat(session_id: str):
    return {"status": "ok"}