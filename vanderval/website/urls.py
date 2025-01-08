from django.urls import path
from .views import  AssignJobView, CustomerJobsView, TaskStatusView, LoginView

urlpatterns = [
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
    path('customer-jobs/<int:customer_id>/', CustomerJobsView.as_view(), name='customer-jobs'),
    path('assign-job/<int:site_id>/', AssignJobView.as_view(), name='assign_job'),
    path('login/', LoginView.as_view(), name='login'),
]
