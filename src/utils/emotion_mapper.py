def detect_math_anxiety(score, attempts):
    """
    Logika Sederhana (Rule-Based) untuk mendeteksi kecemasan:
    - Percobaan banyak + Nilai rendah = Cemas Tinggi (Frustasi)
    - Percobaan sedikit + Nilai rendah = Cemas Sedang (Bingung)
    - Percobaan banyak + Nilai tinggi = Cemas Rendah (Gigih)
    - Percobaan sedikit + Nilai tinggi = Percaya Diri (Flow)
    """
    if score < 50:
        if attempts > 3:
            return "Tinggi (Frustasi)"
        else:
            return "Sedang (Bingung)"   
    elif score < 80:
        if attempts > 3:
            return "Sedang (Berusaha)"
        else:
            return "Rendah (Normal)"
    else:
        # Nilai Tinggi
        if attempts > 2:
            return "Rendah (Teliti)"
        else:
            return "Percaya Diri (Flow)"