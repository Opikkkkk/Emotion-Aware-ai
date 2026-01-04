from flask import Blueprint, render_template, request, session, redirect, url_for
from utils.data_loader import load_logs

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# =========================
# LOGIN TEACHER
# =========================
@teacher_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "admin123":  # password sederhana
            session["is_teacher"] = True
            return redirect(url_for("teacher.dashboard"))
        else:
            return render_template(
                "teacher_login.html",
                error="Password Salah!"
            )

    return render_template("teacher_login.html")


# =========================
# DASHBOARD TEACHER
# =========================
@teacher_bp.route("/dashboard")
def dashboard():
    # Proteksi halaman dashboard
    if not session.get("is_teacher"):
        return redirect(url_for("teacher.login"))

    logs = load_logs()

    # 1. Statistik Sederhana
    total_students = len(logs)
    avg_score = 0
    anxiety_counts = {
        "Tinggi": 0,
        "Sedang": 0,
        "Rendah": 0
    }

    if total_students > 0:
        total_score = sum(log.get("score", 0) for log in logs)
        avg_score = round(total_score / total_students, 2)

        # Hitung sebaran anxiety
        for log in logs:
            emotion_text = log.get("emotion", "")
            if "Tinggi" in emotion_text:
                anxiety_counts["Tinggi"] += 1
            elif "Sedang" in emotion_text:
                anxiety_counts["Sedang"] += 1
            else:
                anxiety_counts["Rendah"] += 1

    return render_template(
        "dashboard.html",
        logs=logs,
        stats={
            "total": total_students,
            "avg": avg_score,
            "anxiety": anxiety_counts
        }
    )
