import os
from dotenv import load_dotenv
from pymongo import MongoClient

def show_logs():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("MONGO_URI not found!")
        return

    client = MongoClient(MONGO_URI)
    db = client["chat_logs_db"]
    collection = db["CoreBotChatLogs"]

    logs = list(collection.find())
    print(f"Found {len(logs)} entries in CoreBotChatLogs:")
    print("=" * 60)
    for i, log in enumerate(logs):
        print(f"--- Entry #{i + 1} ---")
        print(f"ID: {log.get('_id')}")
        print(f"Session ID: {log.get('session_id')}")
        print(f"Question: {log.get('question')}")
        print(f"Answer: {log.get('answer')}")
        print(f"Sources: {log.get('sources')}")
        print(f"Timestamp: {log.get('timestamp')}")
        print("=" * 60)

if __name__ == "__main__":
    show_logs()
