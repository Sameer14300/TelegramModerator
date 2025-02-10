from pymongo import MongoClient
from config import MONGODB_URI
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client.telegram_bot
            self.warnings = self.db.warnings
            self.groups = self.db.groups
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_user_warnings(self, user_id: int, chat_id: int) -> int:
        warning = self.warnings.find_one({"user_id": user_id, "chat_id": chat_id})
        return warning["count"] if warning else 0

    def add_warning(self, user_id: int, chat_id: int, username: str = None):
        result = self.warnings.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$inc": {"count": 1}, "$set": {"username": username}},
            upsert=True
        )
        return self.get_user_warnings(user_id, chat_id)

    def remove_warning(self, user_id: int, chat_id: int) -> int:
        warning = self.warnings.find_one({"user_id": user_id, "chat_id": chat_id})
        if warning and warning["count"] > 0:
            self.warnings.update_one(
                {"user_id": user_id, "chat_id": chat_id},
                {"$inc": {"count": -1}}
            )
        return self.get_user_warnings(user_id, chat_id)

    def get_all_groups(self):
        return list(self.groups.find({}))

    def add_group(self, chat_id: int, title: str):
        self.groups.update_one(
            {"chat_id": chat_id},
            {"$set": {"title": title, "settings": {"scan_bio": True}}},
            upsert=True
        )

    def remove_group(self, chat_id: int):
        self.groups.delete_one({"chat_id": chat_id})

    def get_group_settings(self, chat_id: int):
        group = self.groups.find_one({"chat_id": chat_id})
        return group.get("settings", {"scan_bio": True}) if group else {"scan_bio": True}

    def update_group_settings(self, chat_id: int, settings: dict):
        self.groups.update_one(
            {"chat_id": chat_id},
            {"$set": {"settings": settings}},
            upsert=True
        )