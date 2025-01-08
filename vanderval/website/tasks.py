import logging
from time import sleep

from .models import Site, UserRecords, Job
from .jobs import job_types  # Assuming this stores job execution times
from .customers import customer_types  # Assuming this stores customer types
from celery import shared_task
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Function to calculate the execution time based on job type and customer type
def calculate_execution_time(job_type, customer_type):
    # Fetch the base execution time for the given job type
    base_execution_time = job_types.get(job_type)
    # Get customer factor multiplier
    customer_factor = customer_types.get(customer_type, 1)
    
    # Calculate and return total execution time
    if base_execution_time:
        return base_execution_time * customer_factor
    else:
        return None  # Return None if the job type is invalid


# Define a shared Celery task for dynamic task execution
@shared_task
def execute_job( site_id: int, job_id: int):
    try:
        # Retrieve the job using task_id
        job = Job.objects.get(id=job_id)
        

        job.status = "IN_PROGRESS"
        job.save()
        
  
        logger.info(f"Job status: {job.status}")  # This will ensure logging is captured

        # Fetch the site and customer type
        site = Site.objects.get(id=site_id)
        customer_type = site.customer_type  # Assuming 'low', 'medium', 'high'
        
        # Calculate execution time based on job type and customer type
        execution_time = calculate_execution_time(job.job_type, customer_type)
        
        if execution_time is None:
            raise ValueError(f"Invalid job type: {job.job_type}")

        # Process records (simulated by sleep)
        records = UserRecords.objects.filter(site=site)
        for record in records:
            sleep(execution_time)  # Simulate task execution
            logger.info(f"{job.job_type}: {record.name} processed with execution time {execution_time}s")

        # After job completion, update the status to COMPLETED
        job.status = "COMPLETED"
        job.result = "Job completed successfully"
        
        job.save()

    except Exception as e:
        # If an error occurs, update job status to FAILED
        job.status = "FAILED"
        job.result = str(e)  # Store the error message in result
        job.save()
        logger.error(f"Error executing job: {str(e)}")
        raise  # Re-raise the exception to mark the task as failed


# Existing tasks, updated to use dynamic task execution
@shared_task
def task_01(site_id: int):
    return execute_job(site_id, 'type_1')

@shared_task
def task_02(site_id: int):
    return execute_job(site_id, 'type_2')

@shared_task
def task_03(site_id: int):
    return execute_job(site_id, 'type_3')

@shared_task
def task_04(site_id: int):
    return execute_job(site_id, 'type_4')

@shared_task
def task_05(site_id: int):
    return execute_job(site_id, 'type_5')
