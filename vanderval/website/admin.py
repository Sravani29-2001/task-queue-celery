from django.contrib import admin
from .models import Site, UserRecords, Job

# Customize the Site model in the Django Admin
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'url', 'description', 'get_record_capacity')
    list_filter = ('record_capicity',)
    search_fields = ('name', 'domain', 'description')
    
    # Method to display record capacity as text
    def get_record_capacity(self, obj):
        return obj.get_record_capicity_display()
    get_record_capacity.short_description = 'Record Capacity'
class JobAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = ('task_id', 'site', 'job_type', 'status', 'created_at', 'result')

    # Add filters for easier searching in the admin panel
    list_filter = ('status', 'job_type', 'site')

    # Enable search functionality
    search_fields = ('task_id', 'job_type', 'result')

    # Optionally add ordering for the job list
    ordering = ('-created_at',)

    # Add pagination (if necessary)
    list_per_page = 20
# Customize the UserRecords model in the Django Admin
class UserRecordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'site', 'is_active')
    list_filter = ('is_active', 'site')
    search_fields = ('name', 'email', 'phone', 'address', 'site__name')
    ordering = ('-is_active',)  # Order by active status first
    
    # Optionally, include a method to display date of birth in a readable format
    def dob_display(self, obj):
        return obj.dob.strftime('%Y-%m-%d') if obj.dob else ''
    dob_display.short_description = 'Date of Birth'

# Register the models with the customized admin
admin.site.register(Site, SiteAdmin)
admin.site.register(UserRecords, UserRecordsAdmin)
admin.site.register(Job,JobAdmin)
