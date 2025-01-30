import json
from flask import Flask, redirect, render_template, request
import calendar_module as cm

app = Flask(__name__)
exam_better_json = cm.BetterJson("exams.json")
interactable = cm.ExamInteractable(exam_better_json)

@app.route("/")
def index():
    return render_template(
        "welcome.html",
        image_address=""
    )

@app.route("/user/")
def user():
    return render_template(
        "user.html",
        image_address="images/mountain1.jpg"
    )

@app.route("/user/create/<name>/", methods=("GET", "POST"))
def create_user(name):
    if name in list(exam_better_json.get("users").keys()):
        return redirect(f"/exams/{name}")
    if request.method == "POST":
        print("posted")
        selected_subject_list = [subject.lower() for subject in request.form.getlist("subjects")]
        exam_better_json.set(f"users.{name}", selected_subject_list)
        exam_better_json.commit()
        return redirect(f"/exams/{name}")
    return render_template(
        "user-create.html",
        name=name,
        available_subjects=exam_better_json.get("subjects"),
        image_address="images/mountain1.jpg"
    )

@app.route("/exams/<name>/")
def exams(name):
    date_list = ["10/02", "11/02", "12/02", "13/02", "14/02", "24/02", "25/02", "26/02", "27/02", "28/02"]
    users_exams = interactable.get_user(name, date_list)
    print(users_exams)
    if users_exams == ():
        return redirect(f"/user/create/{name}")
    return render_template(
        "calendar.html",
        name=name,
        dates=date_list,
        day_list=users_exams,
        image_address="images/trees1.jpg"
    )

@app.route("/admin/")
def admin():
    return render_template(
        "admin.html",
        userlist=list(exam_better_json.get("users").keys()),
        image_address="images/bird1.jpg"
    )

@app.route("/admin/delete/<name>")
def admin_delete(name: str):
    exam_better_json.remove(f"users.{name}")
    return redirect("/admin/")