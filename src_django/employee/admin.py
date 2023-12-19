from django.contrib import admin
from employee.models import Employee, DynamicColumn


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "contact_info",
        "location",
        "company",
        "department",
        "position",
        "status",
        "auth_user",
    ]
    fields = list_display


@admin.register(DynamicColumn)
class DynamicColumnAdmin(admin.ModelAdmin):
    fields = [
        "company",
        "fields",
    ]
    list_display = fields
