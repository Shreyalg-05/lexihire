from flask import Flask, request, jsonify, send_from_directory
from engine.resume_engine import ResumeEngine
from engine.search_engine import SearchEngine
from engine.shortlist_engine import ShortlistEngine
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


# ==================================================
# RESUME UPLOAD
# ==================================================
@app.route("/resume/upload", methods=["POST"])
def upload_resume():
    print("UPLOAD ROUTE HIT")

    files = request.files.getlist("resume") or request.files.getlist("file")

    if not files:
        return jsonify({"error": "at least one resume file required"}), 400

    results = []

    for file in files:
        result = ResumeEngine.upload_resume(file)
        results.append(result)

    return jsonify({
        "message": "Resumes uploaded successfully",
        "uploaded_count": len(results),
        "results": results
    })


# ==================================================
# VIEW RESUME (INLINE DISPLAY)
# ==================================================
@app.route("/resume/view/<int:user_id>/<filename>")
def view_resume(user_id, filename):
    folder = os.path.join("uploads", "resumes", str(user_id))
    return send_from_directory(folder, filename)


# ==================================================
# DOWNLOAD RESUME (FORCE DOWNLOAD)
# ==================================================
@app.route("/resume/download/<int:user_id>/<filename>")
def download_resume(user_id, filename):
    folder = os.path.join("uploads", "resumes", str(user_id))
    return send_from_directory(
        folder,
        filename,
        as_attachment=True  # 🔥 Forces download
    )


# ==================================================
# SEARCH
# ==================================================
@app.route("/search", methods=["GET"])
def search():
    skills = request.args.get("skills")
    experience = request.args.get("experience")
    name = request.args.get("name")

    result = SearchEngine.search(
        skills=skills,
        experience=experience,
        name=name
    )

    return jsonify(result)


# ==================================================
# SHORTLIST
# ==================================================
@app.route("/shortlist", methods=["POST"])
def shortlist():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    status = data.get("status")

    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({"error": "valid user_id required"}), 400

    if not isinstance(status, str):
        return jsonify({"error": "status must be string"}), 400

    result = ShortlistEngine.update_status(user_id, status)
    return jsonify(result)


# ==================================================
# VIEW SHORTLIST
# ==================================================
@app.route("/shortlist", methods=["GET"])
def view_shortlist():
    result = ShortlistEngine.get_shortlisted()
    return jsonify(result)


# ==================================================
# RUN APP
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)
