from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from rest_framework import status
from .models import Site, Job, UserRecords
from .jobs import job_types
from .customers import customer_types
from .tasks import execute_job  # Celery task
from celery.result import AsyncResult
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class AssignJobView(APIView):
    def post(self, request, site_id):
        try:
            # Get site by ID
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            raise NotFound(detail="Site not found")

        # Get job_type from the request body
        job_type = request.data.get('job_type')

        # Validate job_type
        if job_type not in job_types:
            return Response({"error": "Invalid job type"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the execution time based on job_type
        execution_time = job_types.get(job_type)

        # Get the actual customer_type from the site model (record_capacity)
        customer_type = site.record_capicity  # This should return Low, Medium, or High

        # Fetch the customer factor based on customer_type
        customer_factor = customer_types.get(customer_type, 1)

        # Apply customer factor to the execution time
        total_execution_time = execution_time * customer_factor

        # Generate a task ID (this can be used to track the job in Job model)
           # Create a new job record in the Job model
        job = Job.objects.create(
            site=site,
    
            job_type=job_type,
            status='PENDING',  # Initially, job status is "PENDING"
        )
        task_id = execute_job.apply_async((site.id, job.id)).id 
 
        job.task_id=task_id 
        job.save()

     

        # Return response with the task ID and execution time
        return Response({
            "site": site.name,
            "job_type": job_type,
            "job_status": job.status,
            "execution_time": total_execution_time,
            "task_id": task_id,  # Returning task_id in response
            "record_capacity": dict(Site.RECORD_CAPACITY_CHOICES).get(customer_type)
        }, status=status.HTTP_202_ACCEPTED)



class TaskStatusView(APIView):

    def get(self, request, task_id):
        """
        Endpoint to get the status of a task by its task ID.
        """
        task_result = AsyncResult(task_id)

        if task_result.state == 'PENDING':
            status = 'Task is pending'
        elif task_result.state == 'STARTED':
            status = 'Task has started'
        elif task_result.state == 'SUCCESS':
            status = f'Task completed successfully: {task_result.result}'
        elif task_result.state == 'FAILURE':
            status = f'Task failed: {task_result.result}'
        else:
            status = 'Unknown task state'

        return Response({
            "task_id": task_id,
            "status": status
        })
    
class CustomerJobsView(APIView):
    def get(self, request, customer_id):
        """
        Endpoint to get all jobs for a customer by customer ID.
        """
        user_records = UserRecords.objects.get(id=customer_id)
        try:
            site = user_records.site  # Assuming you have a 'customer' FK in Site
        except Site.DoesNotExist:
            raise NotFound(detail="Customer not found.")

        # Retrieve all jobs related to this site
        jobs = Job.objects.filter(site=site)
        
        # Prepare job data for response
        job_data = [{
            "task_id": job.task_id,
            "job_type": job.job_type,
            "status": job.status,
            "result": job.result,
            "created_at": job.created_at
        } for job in jobs]

        return Response({
            "customer_id": customer_id,
            "jobs": job_data
        })
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Get or create a token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)