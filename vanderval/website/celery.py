from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanderval.settings')  # Replace 'your_project_name' with your actual project name

app = Celery('vanderval')

# Configure Redis as the broker
app.conf.broker_url = 'redis://localhost:6379/0'  # Use Redis instead of RabbitMQ

# (Optional) If you want to store task results in Redis
app.conf.result_backend = 'redis://localhost:6379/0'

# Autodiscover tasks in installed Django apps
app.autodiscover_tasks(['website'])
