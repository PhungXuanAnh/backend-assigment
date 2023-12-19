from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from employee.models import Employee, DynamicColumn, Location, Position, Company, Department


class EmployeeListAPIViewTest(APITestCase):
    url = reverse("api_list_employee")

    def setUp(self):
        super().setUp()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin")
        self.admin_client = APIClient()
        self.admin_client.login(username="admin", password="admin")

        department_manager_user = User.objects.create_user(
            username="department_manager",
            password="1234",
        )
        self.department_manager_client = APIClient()
        self.department_manager_client.login(username="department_manager", password="1234")

        self.first_name = "first name"
        self.last_name = "last name"
        self.contact_info = "123"
        self.location = Location.objects.create(name="Singapo")
        self.company = Company.objects.create(name="company-1")
        self.department = Department.objects.create(name="HR", company=self.company)
        self.manager_position = Position.objects.create(name="manager")
        self.staff_position = Position.objects.create(name="staff")
        self.status = Employee.ACTIVE

        # create 1 department manager employee for current company
        self.department_manager = Employee.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            contact_info=self.contact_info,
            location=self.location,
            company=self.company,
            department=self.department,
            position=self.manager_position,
            status=self.status,
            auth_user=department_manager_user,
        )

        # create 5 employee of the current company
        for i in range(5):
            Employee.objects.create(
                company=self.company,
            )

        # create 5 employee of the other company
        for i in range(5):
            Employee.objects.create(company=Company.objects.create(name="other-company"))

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_403_permission(self):
        response = self.department_manager_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supersuser_list_all_employee(self):
        response = self.admin_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["count"], 11)

    def test_superuser_filter_1_company(self):
        response = self.admin_client.get(self.url + f"?company={self.company.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["count"], 6)

    def test_department_manager_filter_current_company(self):
        response = self.department_manager_client.get(self.url + f"?company={self.company.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["count"], 6)

    def test_filter_correct_data_and_return_all_columns(self):
        response = self.department_manager_client.get(
            self.url
            + f"?company={self.company.name}&department={self.department.name}&postion={self.manager_position.name}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        data = response.data["results"][0]
        self.assertEqual(data["department"], self.department.name)
        self.assertEqual(data["position"], self.manager_position.name)
        self.assertEqual(data["status"], self.status)
        self.assertEqual(data["location"], self.location.name)
        self.assertEqual(data["first_name"], self.department_manager.first_name)
        self.assertEqual(data["last_name"], self.department_manager.last_name)
        self.assertEqual(data["contact_info"], self.department_manager.contact_info)

    def test_filter_correct_data_and_return_correct_dynamic_columns(self):
        fields = "department,position,location"
        DynamicColumn.objects.create(company=self.company, fields=fields)
        
        response = self.department_manager_client.get(
            self.url
            + f"?company={self.company.name}&department={self.department.name}&postion={self.manager_position.name}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        data = response.data["results"][0]
        self.assertEqual(data["department"], self.department.name)
        self.assertEqual(data["position"], self.manager_position.name)
        self.assertEqual(data["status"], self.status)
        self.assertEqual(data["location"], self.location.name)
        self.assertEqual(data["first_name"], self.department_manager.first_name)
        self.assertEqual(data["last_name"], self.department_manager.last_name)
        
        self.assertNotIn("contact_info", data)
