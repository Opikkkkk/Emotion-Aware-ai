import json
import pandas as pd

def load_questions():
    return pd.read_csv("data/questions.csv")

def load_logs():
    with open("data/student_logs.json") as f:
        return json.load(f)
