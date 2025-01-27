from flask import Flask, render_template
import calendar_module as cm

app = Flask(__name__)
interactable = cm.ExamInteractable(cm.BetterJson("exams.json"))

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/exams/<name>/")
def exams(name):
    first_week = ["10/02", "11/02", "12/02", "13/02", "14/02"]
    exam_list = interactable.get_user(name, first_week)
    return render_template(
        "calendar.html",
        name=name,
        dates=first_week,
        week=exam_list
    )
