from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
import os

from database import (
    init_db,
    register_user,
    login_user,
    save_analysis,
    get_user_analyses
)

from resume_parser import extract_text
from nlp_engine import extract_skills, extract_email, extract_phone
from job_matcher import recommend_jobs
from llm_engine import analyze_resume
from ats_engine import calculate_ats_score

app = Flask(__name__)
app.secret_key = "resume_ai_project_secret"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("database", exist_ok=True)

init_db()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill all required fields.")
            return redirect("/register")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect("/register")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.")
            return redirect("/register")

        if register_user(name, email, password):
            flash("Registration successful. Please login.")
            return redirect("/login")

        flash("Email already registered.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = login_user(email, password)

        if user:
            session["user_id"] = user[0]
            session["name"] = user[1]
            return redirect("/dashboard")

        flash("Invalid email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    analyses = get_user_analyses(session["user_id"])

    return render_template(
        "dashboard.html",
        name=session["name"],
        analyses=analyses
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    if "user_id" not in session:
        return redirect("/login")

    file = request.files.get("resume")
    job_role = request.form.get("job_role", "All Jobs")

    if not file or file.filename == "":
        flash("Please upload a resume.")
        return redirect("/dashboard")

    if not allowed_file(file.filename):
        flash("Only PDF, DOCX and TXT files are allowed.")
        return redirect("/dashboard")

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    text = extract_text(filepath)

    if not text.strip():
        flash("Could not extract text from the resume.")
        return redirect("/dashboard")

    skills = extract_skills(text)

    recommendations = recommend_jobs(skills)

    if job_role != "All Jobs":

        selected = [
            job for job in recommendations
            if job["title"].lower() == job_role.lower()
        ]

        if selected:
            recommendations = selected + [
                job for job in recommendations
                if job["title"].lower() != job_role.lower()
            ]

    top = recommendations[0] if recommendations else {
        "title": "No match",
        "score": 0,
        "matched": [],
        "missing": []
    }

    ats_score, ats_details = calculate_ats_score(text, skills)

    llm = analyze_resume(
        text,
        skills,
        recommendations
    )

    save_analysis(
        session["user_id"],
        filename,
        job_role,
        top["score"],
        skills,
        top["missing"],
        llm
    )

    return render_template(
        "result.html",
        filename=filename,
        email=extract_email(text),
        phone=extract_phone(text),
        skills=skills,
        recommendations=recommendations,
        top=top,
        ats_score=ats_score,
        ats_details=ats_details,
        llm=llm
    )


if __name__ == "__main__":
    app.run(debug=True)