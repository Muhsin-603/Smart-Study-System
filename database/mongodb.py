"""
MongoDB Storage and Authentication Module for Smart Study Recommendation System
Manages students and academic records collections with secure salted password hashing.
"""

import os
import hashlib
import secrets
from typing import Optional, Tuple, Dict, Any, List
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://muhsin:Muhsin12345@cluster0.a8wl8vu.mongodb.net/smart_study_db?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = os.getenv("DB_NAME", "smart_study_db")

_client: Optional[MongoClient] = None


def get_mongo_client() -> MongoClient:
    """Return a singleton MongoClient instance with 5s timeout."""
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    return _client


def check_connection() -> Tuple[bool, str]:
    """Test ping to MongoDB server. Returns (is_connected, message)."""
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True, "Successfully connected to MongoDB Atlas."
    except Exception as e:
        return False, str(e)


def get_database():
    """Retrieve database handle."""
    client = get_mongo_client()
    return client[DB_NAME]


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Secure password hashing using PBKDF2 with SHA-256 and unique salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return hashed, salt


def verify_password(stored_hash: str, salt: str, provided_password: str) -> bool:
    """Verify if provided password matches stored salted hash."""
    hashed, _ = hash_password(provided_password, salt)
    return secrets.compare_digest(hashed, stored_hash)


def register_student(student_id: str, name: str, password: str, elective: str) -> Tuple[bool, str]:
    """Register a new student."""
    try:
        db = get_database()
        students_col = db["students"]

        student_id_clean = student_id.strip().upper()
        if not student_id_clean or not name.strip() or not password.strip():
            return False, "Student ID, Name, and Password cannot be empty."

        existing = students_col.find_one({"student_id": student_id_clean})
        if existing:
            return False, f"Student ID '{student_id_clean}' is already registered."

        hashed_pw, salt = hash_password(password.strip())
        student_doc = {
            "student_id": student_id_clean,
            "name": name.strip(),
            "password_hash": hashed_pw,
            "salt": salt,
            "elective": elective,
            "overall_attendance": 85.0,
            "overall_study_hours": 2.5,
            "previous_overall_marks": 28.0
        }
        students_col.insert_one(student_doc)

        # Initialize default records for the 5 subjects
        from data.generate_dataset import CORE_SUBJECTS
        initial_subjects = CORE_SUBJECTS + [elective]
        records_col = db["academic_records"]

        records = []
        for subj in initial_subjects:
            records.append({
                "student_id": student_id_clean,
                "subject": subj,
                "previous_marks": 26.0,
                "internal_marks": 24.0,
                "attendance": 82.0,
                "study_hours": 2.0,
                "actual_final_marks": None
            })
        records_col.insert_many(records)

        return True, "Registration successful! You can now log in."
    except PyMongoError as e:
        return False, f"Database error during registration: {str(e)}"


def authenticate_student(student_id: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Authenticate student by ID and password."""
    try:
        db = get_database()
        students_col = db["students"]
        student_id_clean = student_id.strip().upper()

        student = students_col.find_one({"student_id": student_id_clean})
        if not student:
            return False, None, "Invalid Student ID or student does not exist."

        if verify_password(student.get("password_hash", ""), student.get("salt", ""), password.strip()):
            return True, student, "Login successful."
        else:
            return False, None, "Incorrect password."
    except Exception as e:
        return False, None, f"Database connection issue: {str(e)}"


def get_student_profile(student_id: str) -> Optional[Dict[str, Any]]:
    """Fetch student profile by ID."""
    try:
        db = get_database()
        return db["students"].find_one({"student_id": student_id.strip().upper()})
    except Exception:
        return None


def update_student_profile(student_id: str, name: str, elective: str, overall_att: float, overall_hours: float, prev_marks: float) -> bool:
    """Update profile and elective for a student."""
    try:
        db = get_database()
        student_id_clean = student_id.strip().upper()
        
        current = db["students"].find_one({"student_id": student_id_clean})
        old_elective = current.get("elective") if current else None

        db["students"].update_one(
            {"student_id": student_id_clean},
            {"$set": {
                "name": name.strip(),
                "elective": elective,
                "overall_attendance": float(overall_att),
                "overall_study_hours": float(overall_hours),
                "previous_overall_marks": float(prev_marks)
            }}
        )

        # If elective changed, update the elective record in academic_records
        if old_elective and old_elective != elective:
            records_col = db["academic_records"]
            records_col.delete_one({"student_id": student_id_clean, "subject": old_elective})
            records_col.insert_one({
                "student_id": student_id_clean,
                "subject": elective,
                "previous_marks": 25.0,
                "internal_marks": 25.0,
                "attendance": 80.0,
                "study_hours": 2.0,
                "actual_final_marks": None
            })

        return True
    except Exception:
        return False


def get_student_academic_records(student_id: str) -> List[Dict[str, Any]]:
    """Retrieve all subject records for a given student."""
    try:
        db = get_database()
        records = list(db["academic_records"].find({"student_id": student_id.strip().upper()}))
        for r in records:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        return records
    except Exception:
        return []


def save_student_academic_records(student_id: str, records: List[Dict[str, Any]]) -> bool:
    """Save or update academic records for the student."""
    try:
        db = get_database()
        records_col = db["academic_records"]
        student_id_clean = student_id.strip().upper()

        for rec in records:
            subject = rec["subject"]
            filter_query = {"student_id": student_id_clean, "subject": subject}
            update_data = {
                "student_id": student_id_clean,
                "subject": subject,
                "previous_marks": float(rec.get("previous_marks", 0.0)),
                "internal_marks": float(rec.get("internal_marks", 0.0)),
                "attendance": float(rec.get("attendance", 0.0)),
                "study_hours": float(rec.get("study_hours", 0.0)),
                "actual_final_marks": float(rec["actual_final_marks"]) if rec.get("actual_final_marks") is not None and str(rec.get("actual_final_marks")).strip() != "" else None
            }
            records_col.update_one(filter_query, {"$set": update_data}, upsert=True)
        return True
    except Exception:
        return False


def get_all_students_summary() -> List[Dict[str, Any]]:
    """Admin function: Retrieve all students and their aggregated performance."""
    try:
        db = get_database()
        students = list(db["students"].find({}, {"password_hash": 0, "salt": 0}))
        records = list(db["academic_records"].find())

        student_dict = {}
        for s in students:
            s_id = s.get("student_id")
            s["_id"] = str(s["_id"])
            s["subjects"] = []
            student_dict[s_id] = s

        for r in records:
            s_id = r.get("student_id")
            if s_id in student_dict:
                r["_id"] = str(r["_id"])
                student_dict[s_id]["subjects"].append(r)

        return list(student_dict.values())
    except Exception:
        return []


def get_verified_records_for_retraining() -> List[Dict[str, Any]]:
    """
    Retrieve real student records that have verified 'actual_final_marks'
    for continuous model learning.
    """
    try:
        db = get_database()
        records = list(db["academic_records"].find({
            "actual_final_marks": {"$ne": None, "$exists": True}
        }))
        return records
    except Exception:
        return []


def seed_demo_students_if_empty():
    """Seed initial student accounts for immediate testing and demonstration."""
    try:
        db = get_database()
        if db["students"].count_documents({}) == 0:
            demo_users = [
                {
                    "student_id": "STU101",
                    "name": "Alex Johnson",
                    "password": "password123",
                    "elective": "Artificial Intelligence",
                    "records": [
                        {"subject": "Computer Networks", "previous_marks": 32.0, "internal_marks": 34.0, "attendance": 92.0, "study_hours": 2.5, "actual_final_marks": None},
                        {"subject": "Machine Learning", "previous_marks": 28.0, "internal_marks": 26.0, "attendance": 84.0, "study_hours": 2.0, "actual_final_marks": None},
                        {"subject": "Design and Analysis of Algorithms (DAA)", "previous_marks": 20.0, "internal_marks": 18.0, "attendance": 76.0, "study_hours": 1.2, "actual_final_marks": None},
                        {"subject": "Microcontrollers (MC)", "previous_marks": 30.0, "internal_marks": 32.0, "attendance": 88.0, "study_hours": 2.2, "actual_final_marks": None},
                        {"subject": "Artificial Intelligence", "previous_marks": 25.0, "internal_marks": 27.0, "attendance": 85.0, "study_hours": 2.0, "actual_final_marks": None},
                    ]
                },
                {
                    "student_id": "STU102",
                    "name": "Priya Sharma",
                    "password": "password123",
                    "elective": "Software Project Management",
                    "records": [
                        {"subject": "Computer Networks", "previous_marks": 19.0, "internal_marks": 17.0, "attendance": 72.0, "study_hours": 1.0, "actual_final_marks": 18.0},
                        {"subject": "Machine Learning", "previous_marks": 22.0, "internal_marks": 20.0, "attendance": 78.0, "study_hours": 1.5, "actual_final_marks": 21.0},
                        {"subject": "Design and Analysis of Algorithms (DAA)", "previous_marks": 16.0, "internal_marks": 15.0, "attendance": 70.0, "study_hours": 1.0, "actual_final_marks": 15.0},
                        {"subject": "Microcontrollers (MC)", "previous_marks": 24.0, "internal_marks": 22.0, "attendance": 80.0, "study_hours": 1.5, "actual_final_marks": 23.0},
                        {"subject": "Software Project Management", "previous_marks": 29.0, "internal_marks": 31.0, "attendance": 86.0, "study_hours": 2.0, "actual_final_marks": 32.0},
                    ]
                }
            ]
            for u in demo_users:
                success, _ = register_student(u["student_id"], u["name"], u["password"], u["elective"])
                if success:
                    save_student_academic_records(u["student_id"], u["records"])
            print("Seeded demo student accounts: STU101 and STU102.")
    except Exception as e:
        print(f"Demo seed error: {e}")
