from flask import Blueprint, request, jsonify
from db import get_connection

resume_bp = Blueprint("resume_bp", __name__)

@resume_bp.route("/resume/upload", methods=["POST"])
def upload_resume():
    data = request.json
    user_id = data.get("user_id")
    resume_url = data.get("resume_url")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO resume_details (user_id, resume_url) VALUES (%s, %s)",
        (user_id, resume_url)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Resume uploaded successfully"})
