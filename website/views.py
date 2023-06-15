from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        task = request.form.get("task")
        if len(task) < 2:
            flash("Task is too short", "warning")
        else:
            new_task = Task(task=task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added", "success")
    return render_template("index.html", user=current_user)


@views.route('/done-task')
@login_required
def done_task():
    if request.args:
        args = request.args
        task_id = args.get("value")
        task = Task.query.get(task_id)
        if task:
            if task.user_id == current_user.id:
                task.done_task = task.task
                task.task = None
                db.session.commit()
    return redirect(url_for("views.home"))


@views.route('delete-task')
@login_required
def delete_task():
    if request.args:
        args = request.args
        task_id = args.get("value")
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("views.home"))
