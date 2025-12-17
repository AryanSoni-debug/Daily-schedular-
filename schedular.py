from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models import Task  # Import Task model (optional)
from database import get_session

# Create global scheduler object
scheduler = BackgroundScheduler()

# This function will run when a scheduled task time occurs
def send_reminder(task_id: int):
    print(f"[{datetime.now()}] Reminder: Task ID {task_id} is due!")

# Function to register reminders from DB
def load_tasks_into_scheduler():
    session = get_session()
    tasks = session.query(Task).all()

    for task in tasks:
        if task.date and task.time:
            run_dt = datetime.combine(task.date, task.time)

            # Register reminder
            scheduler.add_job(
                send_reminder,
                trigger='date',
                run_date=run_dt,
                args=[task.id],
                id=f"task_{task.id}",
                replace_existing=True
            )

    session.close()

def start_scheduler():
    load_tasks_into_scheduler()
    scheduler.start()
    print("Scheduler started and tasks loaded.")