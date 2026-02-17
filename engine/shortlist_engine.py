from db.database import Database

class ShortlistEngine:

    VALID_STATUSES = {"shortlisted", "rejected", "pending"}

    @staticmethod
    def update_status(user_id: int, status: str):
        if status not in ShortlistEngine.VALID_STATUSES:
            return {"error": "Invalid status"}

        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO shortlist (user_id, status)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE status=%s
            """,
            (user_id, status, status)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": f"Candidate {status}",
            "user_id": user_id,
            "status": status
        }

    @staticmethod
    def get_shortlisted():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT u.id, u.name, u.skills, u.experience
            FROM shortlist s
            JOIN user_details u ON s.user_id = u.id
            WHERE s.status = 'shortlisted'
            """
        )

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return results
