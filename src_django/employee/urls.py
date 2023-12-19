from django.urls import include, path
from employee.views import EmployeeListAPIView


urlpatterns = [
    path(
        r"employee",
        EmployeeListAPIView.as_view(),
        name="api_list_employee"
    )
]
