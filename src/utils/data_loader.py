# utils/data_loader.py

import json
import os
import pandas as pd

# Mendapatkan path absolut ke folder 'data' (naik 2 level dari utils)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_questions():
    csv_path = os.path.join(DATA_DIR, "questions.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame() # Return kosong jika file tidak ada

def load_logs():
    json_path = os.path.join(DATA_DIR, "student_logs.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
    return []