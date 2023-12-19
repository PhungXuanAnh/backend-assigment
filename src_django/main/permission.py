from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from employee.models import Employee


class ListEmployeePermission(BasePermission):
    message = "You don't specify your company or you don't have permission to list employees of the specified company"

    def has_permission(self, request, view):
        user = request.user
        if not user or isinstance(user, AnonymousUser):
            return False

        if user.is_superuser:
            return True

        employee = Employee.objects.filter(auth_user=user).first()
        if not employee or str(employee.company.name) != request.query_params.get("company"):
            return False

        return True
