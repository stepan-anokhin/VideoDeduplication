import os

from celery import Celery

# Configuration parameters
BROKER = os.environ.get("CELERY_BROKER", "redis://localhost:6379/0")
BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Create application
celery_application = Celery("winnow-pipeline", broker=BROKER, backend=BACKEND, include=["task_queue.tasks"])

if __name__ == "__main__":
    celery_application.start()