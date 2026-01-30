from flask import Blueprint, request, jsonify
from db import get_connection
from engine.resume_engine import extract_skills_experience
from engine.nlp_search import tfidf_search
import re
import os
engine_bp = Blueprint("engine_bp", __name__)
UPLOAD_FOLDER = "uploads/resumes"

def extract_min_experience(query):
    match = re.search(r"(\d+(\.\d+)?)\s+years?", query.lower())
    if match:
        return float(match.group(1))
    return None

@engine_bp.route("/engine/process", methods=["POST"])
def process_resume():
    data = request.json
    user_id = data.get("user_id")
    resume_text = data.get("resume_text")

    skills, experience = extract_skills_experience(resume_text)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE user_details SET skills=%s, experience=%s WHERE id=%s """, (skills, experience, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Skills and experience stored",
        "skills": skills,
        "experience": experience
    })
@engine_bp.route("/admin/search", methods=["GET"])
def admin_search():
    skill = request.args.get("skill")
    min_exp = request.args.get("min_exp", 0)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """ SELECT id, name, skills, experience FROM user_details WHERE skills LIKE %s AND experience >= %s """

    cursor.execute(query, (f"%{skill}%", float(min_exp)))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(results)
@engine_bp.route("/admin/nlp-search", methods=["POST"])
def admin_nlp_search():
    data = request.json

    if not data or "query" not in data:
        return jsonify({"error": "Query text is required"}), 400

    query = data["query"]
    min_exp = extract_min_experience(query)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if min_exp is not None:
        cursor.execute(""" SELECT id, name, skills, experience FROM user_details WHERE experience >= %s""", (min_exp,))
    else:
        cursor.execute("SELECT id, name, skills, experience FROM user_details")

    users = cursor.fetchall()
    cursor.close()
    conn.close()

    documents = [
        f"{u['skills']} {u['experience']} years experience"
        for u in users
    ]

    scores = tfidf_search(query, documents)

    results = []
    for i, user in enumerate(users):
        user["score"] = round(float(scores[i]), 3)
        results.append(user)

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)
@engine_bp.route("/admin/shortlist", methods=["POST"])
def shortlist_candidate():
    data = request.json
    user_id = data.get("user_id")
    status = data.get("status")  # shortlisted or rejected

    if not user_id or status not in ["shortlisted", "rejected"]:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check if already exists
    cursor.execute("SELECT id FROM shortlist WHERE user_id = %s",(user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE shortlist SET status = %s WHERE user_id = %s",(status, user_id))
    else:
        cursor.execute("INSERT INTO shortlist (user_id, status) VALUES (%s, %s)",(user_id, status))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Candidate {status} successfully"
    }), 200
@engine_bp.route("/admin/shortlisted", methods=["GET"])
def get_shortlisted():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT u.id, u.name, u.skills, u.experience, s.status FROM user_details u JOIN shortlist s ON u.id = s.user_id WHERE s.status = 'shortlisted'""")

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)
@engine_bp.route("/admin/rejected", methods=["GET"])
def get_rejected():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT u.id, u.name, u.skills, u.experience, s.status FROM user_details u JOIN shortlist s ON u.id = s.user_id WHERE s.status = 'rejected'""")

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)
@engine_bp.route("/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files or "user_id" not in request.form:
        return jsonify({"error": "Missing file or user_id"}), 400

    file = request.files["resume"]
    user_id = request.form["user_id"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"user_{user_id}.pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    resume_url = f"/uploads/resumes/{filename}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resume_details (user_id, resume_url) VALUES (%s, %s)",(user_id, resume_url))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume_url": resume_url
    })

