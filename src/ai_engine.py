from utils.emotion_mapper import detect_math_anxiety

def analyze_student(score, attempts):
    anxiety = detect_math_anxiety(score, attempts)

    return {
        "score": score,
        "attempts": attempts,
        "anxiety": anxiety
    }
