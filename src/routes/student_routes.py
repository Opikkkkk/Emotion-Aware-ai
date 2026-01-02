from flask import Blueprint, request, redirect, url_for, session, render_template
from utils.data_loader import load_questions # Import loader

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/start", methods=["POST"])
def start():
    name = request.form.get("name")
    grade = request.form.get("grade")
    style = request.form.get("style")

    if not name or not grade or not style:
        return redirect(url_for("index"))

    session["student"] = {
        "name": name,
        "grade": grade,
        "style": style
    }

    return redirect(url_for("student.learn"))

@student_bp.route("/learn")
def learn():
    if "student" not in session:
        return redirect(url_for("index"))

    student = session["student"]
    
    # 1. Load semua pertanyaan
    df = load_questions()
    
    # 2. Filter pertanyaan sesuai Grade & Style siswa
    # (Contoh: Ambil soal untuk 'SD' dan 'visual')
    try:
        filtered_questions = df[
            (df['grade'] == student['grade']) & 
            (df['style'] == student['style'])
        ]
        
        # Ubah ke format dictionary agar bisa dibaca HTML
        questions_list = filtered_questions.to_dict('records')
    except Exception as e:
        print(f"Error loading questions: {e}")
        questions_list = []

    # 3. Kirim data 'questions' ke template
    return render_template("learn.html", student=student, questions=questions_list)