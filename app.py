from flask import Flask
from routes.resume_routes import resume_bp
from routes.engine_routes import engine_bp
from flask import send_from_directory
app = Flask(__name__)

app.register_blueprint(resume_bp)
app.register_blueprint(engine_bp)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB


#Health Check Route
@app.route("/")
def home():
    return "LexiHire backend is running"
@app.route("/uploads/resumes/<filename>")
def get_resume(filename):
    return send_from_directory("uploads/resumes", filename)


if __name__ == "__main__":
    app.run(debug=True)



