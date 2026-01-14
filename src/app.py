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

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'student_logs.json')
CSV_FILE = os.path.join(DATA_DIR, 'questions.csv')

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'rahasia_tubes_ai'

# --- FUNGSI UTAMA ---

def generate_smart_recommendation(score, emotion, grade):
    """
    Sistem Pakar: Menggabungkan Skor Akademik + Emosi untuk saran presisi.
    """
    advice = ""
    
    # KATEGORI 1: NILAI RENDAH (< 50)
    if score < 50:
        if emotion in ['sad', 'fear', 'angry']:
            advice = "🚨 PERLU PERHATIAN KHUSUS: Siswa mengalami kesulitan akademik DAN tekanan emosional. Sarankan sesi konseling atau remedial dengan pendekatan personal (one-on-one)."
        elif emotion in ['happy', 'neutral']:
            advice = "⚠️ MISKONSEPSI: Siswa merasa nyaman/senang tapi nilainya rendah. Kemungkinan siswa meremehkan soal atau salah konsep dasar. Berikan feedback korektif langsung."
        else:
            advice = "📚 REMEDIAL: Fokus pada pengulangan materi dasar dengan metode visual."

    # KATEGORI 2: NILAI SEDANG (50 - 80)
    elif 50 <= score < 80:
        if emotion in ['surprise', 'fear']:
            advice = "💡 PEMANTAPAN: Siswa bisa menjawab tapi terlihat ragu/cemas. Berikan latihan soal serupa untuk membangun kepercayaan diri."
        else:
            advice = "📈 LATIHAN: Pemahaman cukup baik. Tingkatkan level kesulitan soal secara bertahap."

    # KATEGORI 3: NILAI TINGGI (>= 80)
    else:
        if emotion in ['happy', 'neutral']:
            advice = "🏆 PENGAYAAN: Performa sempurna! Siswa siap untuk materi tingkat lanjut (HOTS) atau menjadi tutor sebaya."
        else:
            advice = "🌟 APRESIASI: Nilai bagus tapi siswa tampak tegang. Berikan pujian untuk mengurangi tekanan perfeksionis."

    return advice

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
            print(f"CSV Error: {e}")
    return questions

def save_log(data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except: logs = [] 
    logs.append(data)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def get_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except: return []
    return []

def read_base64_image(base64_string):
    try:
        if ',' in base64_string: base64_string = base64_string.split(',')[1]
        decoded_data = base64.b64decode(base64_string)
        np_data = np.frombuffer(decoded_data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        return img
    except: return None

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    all_questions = load_questions() 

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            grade = request.form.get('grade')
            image_data = request.form.get('face_image')
            
            # --- LOGIKA PENILAIAN (SCORING) ---
            correct_count = 0
            total_questions = 3 # Kita set 3 soal per sesi
            quiz_log = {}

            # Kita cari soal mana yang tadi dikerjakan berdasarkan teks pertanyaannya
            for i in range(1, 4):
                q_text = request.form.get(f'q{i}_text')
                user_ans = request.form.get(f'ans{i}')
                
                # Cari jawaban benar dari database soal
                correct_ans = "N/A"
                status = "❌ Salah"
                
                # Cari soal di database yang teksnya sama
                matching_q = next((item for item in all_questions if item["question"] == q_text), None)
                
                if matching_q:
                    correct_ans = matching_q['correct']
                    if user_ans == correct_ans:
                        correct_count += 1
                        status = "✅ Benar"
                
                quiz_log[f"Soal {i}"] = {
                    "q": q_text,
                    "user": user_ans,
                    "key": correct_ans,
                    "status": status
                }

            # Hitung Nilai Akhir (Skala 100)
            final_score = int((correct_count / total_questions) * 100)

            # --- PROSES AI EMOSI ---
            emotion_indo = "Netral"
            dominant_emotion = "neutral"
            feedback_text = "Analisis selesai."

            if image_data and len(image_data) > 100:
                img = read_base64_image(image_data)
                if img is not None:
                    try:
                        analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
                        if isinstance(analysis, list): analysis = analysis[0]
                        dominant_emotion = analysis['dominant_emotion']
                        
                        map_emo = {'angry':'Marah','disgust':'Jijik','fear':'Takut','happy':'Senang','sad':'Sedih','surprise':'Terkejut','neutral':'Netral'}
                        emotion_indo = map_emo.get(dominant_emotion, dominant_emotion)
                    except: pass
            
            # --- GENERATE REKOMENDASI CERDAS ---
            ai_recommendation = generate_smart_recommendation(final_score, dominant_emotion, grade)
            
            # Feedback untuk siswa
            feedback_text = f"Nilai kamu: {final_score}/100. Emosi: {emotion_indo}."

            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "grade": grade,
                "emotion": emotion_indo,
                "raw_emotion": dominant_emotion,
                "academic_score": final_score, # Simpan nilai
                "recommendation": ai_recommendation,
                "quiz_detail": quiz_log
            }
            save_log(log_entry)

            result = {
                'emotion': emotion_indo, 
                'score': final_score, # Kirim nilai ke frontend
                'feedback': feedback_text
            }

        except Exception as e:
            print(f"Error: {e}")

    return render_template('index.html', result=result, questions_json=json.dumps(all_questions))

@app.route('/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('teacher_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('teacher_login'))
    logs = get_logs()
    
    # Stats
    total = len(logs)
    avg_score = 0
    if total > 0:
        avg_score = round(sum([l.get('academic_score', 0) for l in logs]) / total)
        
    stats = {'total': total, 'avg_score': avg_score}
    logs.reverse()
    return render_template('dashboard.html', logs=logs, stats=stats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('teacher_login'))

if __name__ == '__main__':
    app.run(debug=True)