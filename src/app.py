#app.py
import sys
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

# =====================
# PATH SETUP (CRITICAL)
# =====================
# Pastikan Python bisa menemukan modul di folder saat ini
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Path Absolut untuk Data & Template
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Naik ke root folder
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(DATA_DIR, "student_logs.json")

# Buat folder data jika belum ada
os.makedirs(DATA_DIR, exist_ok=True)

# =====================
# IMPORTS
# =====================
from ai_engine import analyze_student
from adaptive_engine import adapt_learning
from ar_module import get_ar_content
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp

# =====================
# FLASK CONFIG
# =====================
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = "rahasia_tubes_ai_2025" # Ganti dengan random string
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)

# =====================
# HELPER FUNCTIONS
# =====================
def save_log(data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                content = f.read()
                if content:
                    logs = json.loads(content)
        except json.JSONDecodeError:
            logs = []

    logs.append(data)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# =====================
# MAIN ROUTES
# =====================
@app.route("/")
def index():
    # Bersihkan session lama saat ke halaman depan
    session.clear()
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if "student" not in session:
        return redirect(url_for("index"))

    try:
        score = int(request.form["score"])
        attempts = int(request.form["attempts"])
    except ValueError:
        return redirect(url_for("student.learn")) # Error handling jika input kosong

    student = session["student"]

    # 1. AI Engine: Analisis Performa & Emosi
    ai_result = analyze_student(score, attempts)

    # 2. Adaptive Engine: Tentukan Materi Selanjutnya
    adaptive_result = adapt_learning(ai_result, student["style"])

    # 3. AR Module: Tentukan Konten Visual
    ar_content = get_ar_content(adaptive_result["materi"])

    # 4. Bungkus Hasil untuk Session & Log
    session["result"] = {
        "score": score,
        "attempts": attempts,
        "understanding": ai_result["level"],       # Level (Dasar/Menengah/Lanjut)
        "emotion": ai_result["emotion"],           # Emosi (Cemas/Percaya Diri)
        "materi": adaptive_result["materi"],       # Materi selanjutnya
        "recommendation": adaptive_result["recommendation"], # Saran belajar
        "ar": ar_content                           # Data objek AR
    }

    # 5. Simpan Log (Database JSON)
    log_data = {
        "student_name": student["name"],
        "grade": student["grade"],
        "style": student["style"],
        **session["result"]
    }
    save_log(log_data)

    return redirect(url_for("result"))

@app.route("/result")
def result():
    if "result" not in session:
        return redirect(url_for("index"))
    
    return render_template("result.html", result=session["result"])

@app.route("/ar")
def ar():
    if "result" not in session:
        return redirect(url_for("index"))
    
    return render_template("ar.html", ar=session["result"]["ar"])

# =====================
# RUNNER
# =====================
if __name__ == "__main__":
    print(f"🚀 Server berjalan. Buka: http://127.0.0.1:5000")
    print(f"📂 Menggunakan folder data di: {DATA_DIR}")
    app.run(debug=True, port=5000)