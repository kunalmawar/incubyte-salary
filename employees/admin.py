from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'country', 'salary')
    search_fields = ('full_name', 'job_title', 'country')
