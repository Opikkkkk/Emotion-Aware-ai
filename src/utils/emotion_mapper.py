def detect_math_anxiety(score, attempts):
    if score < 60 and attempts > 2:
        return "Tinggi"
    elif score < 75:
        return "Sedang"
    else:
        return "Rendah"
