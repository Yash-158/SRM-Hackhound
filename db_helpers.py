import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to MongoDB."""
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.career_navigator
    return db

def save_user_profile(user_id, profile_data):
    """Save user profile to database."""
    db = get_db_connection()
    users = db.users
    
    # Update if exists, insert if not
    users.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )

def get_user_profile(user_id):
    """Retrieve user profile from database."""
    db = get_db_connection()
    users = db.users
    
    user = users.find_one({"user_id": user_id})
    return user

def save_career_paths(user_id, paths_data):
    """Save generated career paths."""
    db = get_db_connection()
    career_paths = db.career_paths
    
    # Parse string to JSON if needed
    if isinstance(paths_data, str):
        try:
            paths_data = json.loads(paths_data)
        except json.JSONDecodeError:
            # If not valid JSON, store as is
            paths_data = {"raw_response": paths_data}
    
    # Update if exists, insert if not
    career_paths.update_one(
        {"user_id": user_id},
        {"$set": {"paths": paths_data}},
        upsert=True
    )

def save_learning_path(user_id, learning_data):
    """Save generated learning recommendations."""
    db = get_db_connection()
    learning_paths = db.learning_paths
    
    # Parse string to JSON if needed
    if isinstance(learning_data, str):
        try:
            learning_data = json.loads(learning_data)
        except json.JSONDecodeError:
            # If not valid JSON, store as is
            learning_data = {"raw_response": learning_data}
    
    # Update if exists, insert if not
    learning_paths.update_one(
        {"user_id": user_id},
        {"$set": {"recommendations": learning_data}},
        upsert=True
    )