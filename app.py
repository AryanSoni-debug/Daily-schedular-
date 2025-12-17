from flask import Flask, request, jsonify
from database import SessionLocal
from models import Task
from schedular import scheduler
from datetime import datetime

app = Flask(__name__)

# ---------------- HOME ROUTE ---------------- #
@app.route("/")
def home():
    return "<h1>Daily Scheduler API Running Successfully</h1>"


# ---------------- GET ALL TASKS ---------------- #
@app.route("/tasks", methods=["GET"])
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()

    return jsonify([{
        "id": t.id,
        "title": t.title,
        "time": t.time.strftime("%Y-%m-%d %H:%M:%S")
    } for t in tasks])


# ---------------- ADD NEW TASK ---------------- #
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    title = data.get("title")
    time_str = data.get("time")

    try:
        task_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except:
        return jsonify({"error": "Time format must be YYYY-MM-DD HH:MM:SS"}), 400

    db = SessionLocal()
    new_task = Task(title=title, time=task_time)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()

    return jsonify({"message": "Task added", "id": new_task.id})


# ---------------- DELETE TASK ---------------- #
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        return jsonify({"error": "Task not found"}), 404

    db.delete(task)
    db.commit()
    db.close()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True)
