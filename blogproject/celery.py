import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')

# Create the Celery application instance
app = Celery('blogproject')

# Load configuration from Django settings with 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from all registered Django app configs
app.autodiscover_tasks()

# Optional: Add this if you want to debug task discovery
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
