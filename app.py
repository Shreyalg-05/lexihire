from flask import Flask
from routes.resume_routes import resume_bp
from routes.engine_routes import engine_bp

app = Flask(__name__)

app.register_blueprint(resume_bp)
app.register_blueprint(engine_bp)

#Health Check Route
@app.route("/")
def home():
    return "LexiHire backend is running"


if __name__ == "__main__":
    app.run(debug=True)



