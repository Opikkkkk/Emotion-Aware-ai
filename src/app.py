import os
import base64
import cv2
import numpy as np
import json
import csv
from datetime import datetime
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, session, flash
from deepface import DeepFace

# --- 1. KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

LOG_FILE = os.path.join(DATA_DIR, 'student_logs.json')
CSV_FILE = os.path.join(DATA_DIR, 'questions.csv')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'rahasia_tubes_ai'

# --- 2. FUNGSI BANTUAN ---

def read_base64_image(base64_string):
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        decoded_data = base64.b64decode(base64_string)
        np_data = np.frombuffer(decoded_data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"❌ Error Decode: {e}")
        return None

def load_questions():
    questions = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                for row in reader:
                    questions.append(row)
        except Exception as e:
            print(f"❌ Error CSV: {e}")
    return questions

def save_log(data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = [] 
    logs.append(data)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def get_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# --- 3. ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    all_questions = load_questions() 

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            grade = request.form.get('grade')
            image_data = request.form.get('face_image')
            
            quiz_log = {}
            for i in range(1, 4):
                q = request.form.get(f'q{i}_text')
                a = request.form.get(f'ans{i}')
                if q: quiz_log[f"Soal {i}"] = f"{q} (Jawab: {a})"

            emotion_indo = "Tidak Terdeteksi"
            dominant_emotion = "unknown"
            feedback_text = "Wajah tidak terlihat."
            focus_score = 0

            # PROSES AI
            if image_data and len(image_data) > 100:
                img = read_base64_image(image_data)
                if img is not None:
                    try:
                        analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
                        if isinstance(analysis, list): analysis = analysis[0]
                        dominant_emotion = analysis['dominant_emotion']
                        
                        map_emo = {'angry':'Marah','disgust':'Jijik','fear':'Takut','happy':'Senang','sad':'Sedih','surprise':'Terkejut','neutral':'Netral'}
                        emotion_indo = map_emo.get(dominant_emotion, dominant_emotion)

                        # LOGIKA SKOR FOKUS (KECERDASAN EMOSIONAL)
                        # Netral/Senang = Fokus Tinggi
                        if dominant_emotion in ['neutral', 'happy']:
                            focus_score = 95
                            feedback_text = "Kondisi mental sangat prima. Fokus tinggi."
                        elif dominant_emotion == 'surprise':
                            focus_score = 80
                            feedback_text = "Cukup fokus, namun sedikit terkejut."
                        elif dominant_emotion in ['sad', 'fear']:
                            focus_score = 60
                            feedback_text = "Terdeteksi kecemasan. Perlu rileksasi."
                        elif dominant_emotion in ['angry', 'disgust']:
                            focus_score = 40
                            feedback_text = "Tingkat stres tinggi. Disarankan istirahat."
                        else:
                            focus_score = 50

                    except Exception as e:
                        print(f"❌ Error DeepFace: {e}")
            
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "grade": grade,
                "emotion": emotion_indo,
                "raw_emotion": dominant_emotion,
                "focus_score": focus_score, # Data baru untuk dashboard
                "quiz_detail": quiz_log
            }
            save_log(log_entry)

            result = {'emotion': emotion_indo, 'feedback': feedback_text, 'raw': dominant_emotion}

        except Exception as e:
            print(f"❌ Error System: {e}")

    return render_template('index.html', result=result, questions_json=json.dumps(all_questions))

@app.route('/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Login Gagal", "error")
    return render_template('teacher_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('teacher_login'))
    
    logs = get_logs()
    
    # --- LOGIKA ANALITIK DASHBOARD ---
    total_students = len(logs)
    avg_focus = 0
    dominant_mood = "Belum ada data"
    mood_counts = {}

    if total_students > 0:
        # 1. Hitung Rata-rata Fokus
        total_score = sum([log.get('focus_score', 0) for log in logs])
        avg_focus = round(total_score / total_students)

        # 2. Cari Mood Dominan
        emotions = [log.get('emotion', 'Unknown') for log in logs]
        mood_counter = Counter(emotions)
        dominant_mood = mood_counter.most_common(1)[0][0]
        
        # 3. Data untuk Grafik (Persentase)
        for emo, count in mood_counter.items():
            mood_counts[emo] = round((count / total_students) * 100)

    stats = {
        'total': total_students,
        'avg_focus': avg_focus,
        'dominant_mood': dominant_mood,
        'mood_percent': mood_counts
    }

    logs.reverse()
    return render_template('dashboard.html', logs=logs, stats=stats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('teacher_login'))

if __name__ == '__main__':
    app.run(debug=True)