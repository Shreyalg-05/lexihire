from db.database import Database
class ShortlistEngine:

    VALID_STATUSES = {"shortlisted", "rejected", "pending"}

    @staticmethod
    def update_status(user_id: int, status: str):
        status = (status or "").strip().lower()

        if status not in ShortlistEngine.VALID_STATUSES:
            return {"error": "Invalid status"}

        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM user_details WHERE id = %s",
            (user_id,)
        )
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {"error": "User not found"}

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
        import os
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT 
                u.id,
                u.name,
                u.skills,
                u.experience,
                r.resume_url
            FROM shortlist s
            JOIN user_details u ON s.user_id = u.id
            LEFT JOIN resume_details r ON u.id = r.user_id
            WHERE s.status = 'shortlisted'
            ORDER BY u.experience DESC
            """
        )

        results = cursor.fetchall()
        for r in results:
            if r.get("resume_url"):
                r["resume_url"] = os.path.basename(str(r["resume_url"]))
        cursor.close()
        conn.close()

        return results
