def adapt_learning(ai_result, learning_style):
    if ai_result["score"] < 60:
        level = "Dasar"
        materi = "Geometri"
    else:
        level = "Lanjutan"
        materi = "Aljabar"

    return {
        "level": level,
        "materi": materi,
        "style": learning_style,
        "feedback": f"Materi {materi} tingkat {level} untuk gaya belajar {learning_style}"
    }
