from flask import Flask, render_template, request
import os
from ai_engine import analyze_student
from adaptive_engine import adapt_learning
from ar_module import get_ar_content

# Get the parent directory of the src folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'), static_folder=os.path.join(base_dir, 'static'))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ar = None

    if request.method == "POST":
        score = int(request.form["score"])
        attempts = int(request.form["attempts"])
        style = request.form["style"]

        ai_result = analyze_student(score, attempts)
        result = adapt_learning(ai_result, style)
        ar = get_ar_content(result["materi"])

    return render_template("index.html", result=result, ar=ar)

if __name__ == "__main__":
    app.run(debug=True)
