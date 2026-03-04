from flask import Flask, request, jsonify, send_from_directory
from engine.resume_engine import ResumeEngine
from engine.search_engine import SearchEngine
from engine.shortlist_engine import ShortlistEngine
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================================================
# RESUME UPLOAD
# ==================================================
@app.route("/resume/upload", methods=["POST"])
def upload_resume():
    print("UPLOAD ROUTE HIT")

    files = request.files.getlist("resume")

    if not files:
        return jsonify({"error": "at least one resume file required"}), 400
    seen = set()
    files = [f for f in files if not (f.filename in seen or seen.add(f.filename))]
    results = []

    for file in files:
        if not allowed_file(file.filename):
            results.append({
                "filename": file.filename,
                "error": "Unsupported file type"
            })
            continue

        try:
            result = ResumeEngine.upload_resume(file)
        except Exception as e:
            result = {
                "filename": file.filename,
                "error": str(e)
            }

        results.append(result)

    return jsonify({
        "message": "Resumes uploaded successfully",
        "uploaded_count": sum(1 for r in results if "user_id" in r),
        "results": results
    })


# ==================================================
# VIEW RESUME (INLINE DISPLAY)
# ==================================================
from werkzeug.utils import secure_filename
@app.route("/resume/view/<int:user_id>/<filename>")
def view_resume(user_id, filename):
    filename = secure_filename(filename)
    folder = os.path.join("uploads", "resumes", str(user_id))
    return send_from_directory(folder, filename)


# ==================================================
# DOWNLOAD RESUME (FORCE DOWNLOAD)
# ==================================================
@app.route("/resume/download/<int:user_id>/<filename>")
def download_resume(user_id, filename):
    filename = secure_filename(filename)
    folder = os.path.join("uploads", "resumes", str(user_id))
    return send_from_directory(folder, filename)


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

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
# ==================================================
# RUN APP
# ==================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
