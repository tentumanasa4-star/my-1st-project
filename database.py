import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config

class JSONEncoderCustom(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime,)):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class JsonCollection:
    """A lightweight JSON file-backed collection that mimics PyMongo Collection methods."""
    def __init__(self, file_path, name):
        self.file_path = Path(file_path)
        self.name = name
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save_data([])

    def _load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, cls=JSONEncoderCustom)

    def _match_doc(self, doc, query):
        if not query:
            return True
        for key, expected in query.items():
            if key == "$or":
                if not any(self._match_doc(doc, cond) for cond in expected):
                    return False
                continue
            if key == "$and":
                if not all(self._match_doc(doc, cond) for cond in expected):
                    return False
                continue
            
            val = doc.get(key)
            if isinstance(expected, dict):
                for op, op_val in expected.items():
                    if op == "$regex":
                        pattern = re.compile(op_val, re.IGNORECASE)
                        if not pattern.search(str(val or "")):
                            return False
                    elif op == "$in":
                        if val not in op_val:
                            return False
                    elif op == "$ne":
                        if val == op_val:
                            return False
                    elif op == "$gte":
                        if val is None or val < op_val:
                            return False
                    elif op == "$lte":
                        if val is None or val > op_val:
                            return False
            else:
                if str(val) != str(expected):
                    return False
        return True

    def find_one(self, filter=None, projection=None):
        data = self._load_data()
        for doc in data:
            if self._match_doc(doc, filter):
                res = dict(doc)
                if projection and isinstance(projection, dict):
                    if projection.get("password") == 0:
                        res.pop("password", None)
                return res
        return None

    def find(self, filter=None, projection=None):
        data = self._load_data()
        results = []
        for doc in data:
            if self._match_doc(doc, filter):
                res = dict(doc)
                if projection and isinstance(projection, dict):
                    if projection.get("password") == 0:
                        res.pop("password", None)
                results.append(res)
        return results

    def insert_one(self, document):
        data = self._load_data()
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = str(uuid.uuid4())
        elif isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
            
        data.append(doc)
        self._save_data(data)
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc["_id"])

    def update_one(self, filter, update):
        data = self._load_data()
        modified = 0
        matched = 0
        for idx, doc in enumerate(data):
            if self._match_doc(doc, filter):
                matched = 1
                updated_doc = dict(doc)
                if "$set" in update:
                    for k, v in update["$set"].items():
                        updated_doc[k] = v
                if "$inc" in update:
                    for k, v in update["$inc"].items():
                        updated_doc[k] = updated_doc.get(k, 0) + v
                data[idx] = updated_doc
                modified = 1
                break
        if modified:
            self._save_data(data)
        
        class UpdateResult:
            def __init__(self, matched, modified):
                self.matched_count = matched
                self.modified_count = modified
        return UpdateResult(matched, modified)

    def delete_one(self, filter):
        data = self._load_data()
        deleted = 0
        new_data = []
        for doc in data:
            if deleted == 0 and self._match_doc(doc, filter):
                deleted = 1
            else:
                new_data.append(doc)
        if deleted:
            self._save_data(new_data)
        
        class DeleteResult:
            def __init__(self, count):
                self.deleted_count = count
        return DeleteResult(deleted)

    def count_documents(self, filter=None):
        if not filter:
            return len(self._load_data())
        return len(self.find(filter))


class Database:
    """Database wrapper providing collections with auto-fallback to local JSON storage."""
    def __init__(self):
        self.client = None
        self.db = None
        self.mode = "JSON"
        self._init_connection()

    def _init_connection(self):
        try:
            client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=1500)
            # Check server connection
            client.admin.command('ping')
            self.client = client
            self.db = client[Config.DATABASE_NAME]
            self.mode = "MONGODB"
            print(f"[CampusEvents DB] Connected successfully to live MongoDB: {Config.DATABASE_NAME}")
        except Exception as e:
            self.mode = "JSON"
            print(f"[CampusEvents DB] MongoDB server unavailable ({e}). Using local persistent JSON store at {Config.DATA_DIR}")

    def get_collection(self, name):
        if self.mode == "MONGODB" and self.db is not None:
            return self.db[name]
        data_path = Path(Config.DATA_DIR) / f"{name}.json"
        return JsonCollection(data_path, name)

# Global DB Instance
db_manager = Database()

def get_db():
    return db_manager

# Accessible collections
users_col = db_manager.get_collection("users")
events_col = db_manager.get_collection("events")
registrations_col = db_manager.get_collection("registrations")
notifications_col = db_manager.get_collection("notifications")
admins_col = db_manager.get_collection("admins")
