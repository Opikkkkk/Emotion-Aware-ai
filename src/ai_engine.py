# ai_engine.py

from utils.emotion_mapper import detect_math_anxiety

def analyze_student(score, attempts):
    # 1. Deteksi Emosi/Anxiety
    emotion = detect_math_anxiety(score, attempts)

    # 2. Tentukan Level Pemahaman (Rule-Based)
    if score < 60:
        level = "Dasar"
    elif score < 85:
        level = "Menengah"
    else:
        level = "Lanjutan"

    # Return dictionary yang konsisten dengan app.py
    return {
        "score": score,
        "attempts": attempts,
        "emotion": emotion, # Di app.py dipanggil sebagai 'emotion'
        "level": level      # Di app.py dipanggil sebagai 'level'
    }