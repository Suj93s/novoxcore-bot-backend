import os
from dotenv import load_dotenv
from pymongo import MongoClient

def delete_logs():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("MONGO_URI not found!")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client["chat_logs_db"]
        collection = db["CoreBotChatLogs"]

        result = collection.delete_many({})
        print(f"Successfully deleted {result.deleted_count} logs from CoreBotChatLogs.")
    except Exception:
        print("Failed to delete logs. Check your database connection configuration.")

if __name__ == "__main__":
    delete_logs()
