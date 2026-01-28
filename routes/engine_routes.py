from flask import Blueprint, request, jsonify
from db import get_connection
from engine.resume_engine import extract_skills_experience
from engine.nlp_search import tfidf_search
import re
engine_bp = Blueprint("engine_bp", __name__)

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

