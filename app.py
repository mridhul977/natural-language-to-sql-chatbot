
from flask import Flask, render_template, request
from sql_generator import generate_sql
from sql_validator import validate_sql
from database import execute_sql

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    question = ""
    sql = ""
    results = None
    error = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if not question:
            error = "Please enter a question."
        else:
            try:
                sql = generate_sql(question)

                if not validate_sql(sql):
                    error = "The generated SQL was rejected."
                    sql = ""
                else:
                    results = execute_sql(sql)

            except Exception as exc:
                error = f"Request failed: {exc}"

    return render_template(
        "index.html",
        question=question,
        sql=sql,
        results=results,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
