from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
FILE = "expenses.csv"


def init_csv():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "description"])


@app.route("/")
def index():
    expenses = []

    if os.path.exists(FILE):
        with open(FILE) as f:
            reader = csv.reader(f)
            rows = list(reader)

            if rows:
                expenses = rows[1:]  # skip header safely

    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                amount,
                category,
                description
            ])

        return render_template("add_expense.html", success=True)

    return render_template("add_expense.html")


category = request.form["category"].strip().title()


if __name__ == "__main__":
    app.run(debug=True)
