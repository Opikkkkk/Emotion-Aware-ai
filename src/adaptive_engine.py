# adaptive_engine.py

def adapt_learning(ai_result, learning_style):
    score = ai_result["score"]
    level = ai_result["level"]
    
    # Logika Penentuan Materi
    if level == "Dasar":
        materi = "Geometri Dasar"
        saran = "Mari kita ulangi konsep dasar bangun ruang dengan visualisasi."
    elif level == "Menengah":
        materi = "Aljabar Linear"
        saran = "Pemahamanmu cukup baik, coba selesaikan variasi soal ini."
    else:
        materi = "Kalkulus Pengantar" # Contoh SMP tingkat lanjut
        saran = "Luar biasa! Kamu siap untuk tantangan logika yang lebih kompleks."

    # Personalisasi berdasarkan gaya belajar
    if learning_style == "visual":
        saran += " (Gunakan grafik AR untuk membantu)."
    elif learning_style == "auditory":
        saran += " (Coba jelaskan langkah-langkahnya dengan suara keras)."
    elif learning_style == "kinesthetic":
        saran += " (Cobalah memutar objek AR untuk melihat sudut pandang lain)."

    return {
        "materi": materi,
        "style": learning_style,
        "recommendation": saran # Di app.py dipanggil 'recommendation'
    }