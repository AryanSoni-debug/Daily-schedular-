from flask import Flask, request, jsonify
from datetime import datetime

from database import SessionLocal, engine
from models import Base, Task
from schedular import start_scheduler, schedule_task

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
start_scheduler()

@app.post("/add-task")
def add_task():
    data = request.get_json()
    title = data.get("title")
    time_str = data.get("reminder_time")  # format: "YYYY-MM-DDTHH:MM:SS"

    if not title or not time_str:
        return jsonify({"error": "Missing title or reminder_time"}), 400

    reminder_time = datetime.fromisoformat(time_str)

    db = SessionLocal()
    task = Task(title=title, reminder_time=reminder_time)
    db.add(task)
    db.commit()
    db.close()

    return jsonify({"message": "Task scheduled"}), 200

@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    output = [
        {"id": t.id, "title": t.title, "reminder_time": str(t.reminder_time)}
        for t in tasks
    ]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

