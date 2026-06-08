import os
import sys
from dotenv import load_dotenv

# Ensure we can import from backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.api import chat, Query
from pymongo import MongoClient

def run_test():
    load_dotenv()

    questions = [
        "Hi",
        "What is Novox?"
    ]

    print("--- 1. Testing Chat Function ---")
    for q in questions:
        query = Query(question=q)
        response = chat(query)
        print(f"Question: {q}")
        print(f"Answer: {response.get('answer')[:100]}...\n")

    print("--- 2. Verifying MongoDB Logs ---")
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("ERROR: MONGO_URI not found in .env")
        return

    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client["chat_logs_db"]
        collection = db["CoreBotChatLogs"]

        # Fetch latest 2 records
        logs = collection.find().sort("_id", -1).limit(2)
        for log in logs:
            print(f"Logged ID: {log.get('_id')}")
            print(f"Session ID: {log.get('session_id')}")
            print(f"Question: {log.get('question')}")
            print(f"Answer: {log.get('answer')[:100]}...")
            print(f"Sources: {log.get('sources')}")
            print(f"Timestamp: {log.get('timestamp')}")
            print("-" * 50)
    except Exception:
        print("Failed to verify logs. Check your database connection configuration.")

if __name__ == "__main__":
    run_test()
