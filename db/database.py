import mysql.connector
import json
from datetime import datetime
from config import DB_CONFIG


class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(**DB_CONFIG)

    # ⭐ ADD THIS METHOD
    @staticmethod
    def insert_resume(data):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO resume_details
        (name, skills, experience, metadata, email, phone_number, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data.get("name"),
            json.dumps(data.get("skills")),
            json.dumps(data.get("experience")),
            json.dumps(data.get("metadata")),
            data.get("email"),
            data.get("phone"),
            datetime.utcnow()
        ))

        conn.commit()
        cursor.close()
        conn.close()