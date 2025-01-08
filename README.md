## Contributors
- Sravani 
- sannidhikovela47@gmail.com
## Installation
1) Install the required Python packages:
    pip install -r requirements.txt
2) Apply database migrations:
    python manage.py makemigrations
    python manage.py migrate
3) Create a superuser for admin access:
    python manage.py createsuperuser
4) Start the Django development server:
    python manage.py runserver
5) Start the Celery worker:
    celery -A backend_hiring worker --loglevel=info
6) Start Redis
    sudo service redis-server start 

## Features/Changes Added:

Implemented job scheduling and execution using Celery.
Enhanced job status updates (e.g., PENDING, IN_PROGRESS, COMPLETED, FAILED).
Improved database interaction for job tracking.

## Steps to Test the Feature:

## URLs for Testing

Endpoints

## Assign a Job:

Endpoint: /assign-job/<int:site_id>/

Method: POST

Description: Assigns a new job to a site.


## Get Task Status:

Endpoint: /task-status/<str:task_id>/

Method: GET

Description: Retrieves the current status of a specific task.


## View Customer Jobs:

Endpoint: /customer-jobs/<int:customer_id>/

Method: GET

Description: Fetches all jobs associated with a specific customer.

## Login:

Endpoint: /login/

Method: POST

Description: Authenticates a user and provides a session or token.


