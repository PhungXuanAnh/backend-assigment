import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from employee.models import Employee, DynamicColumn, Company, Department, Location, Position


class Command(BaseCommand):
    help = """
        Create 1 employee user to test search employee
        Create sample data for employee table:
        100 companies
            each company has 10 departments
                each departments has 1000 employee
                    status: random in : active, not started, terminated
                    contact_info: increase number
                    first_name: random string
                    last_name: random string
                    location: random string
                    position: random string
    """

    NUMBER_COMPANY = 100
    NUMBER_DEPARTMENT = 10
    NUMBER_EMPLOYEE = 1000
    POSITIONS = [
        "manager",
        "staff"
    ]
    DEPARTMENTS = ["HR", "marketting", "sale", "technical"]
    EXIST_FIELDS = [
        "contact_info",
        "location",
        "company",
        "department",
        "position",
    ]
    LOCATIONS = ["Singapo", "Vietnam", "US", "UK"]

    def __create_companies(self):
        companies = []
        for c in range(self.NUMBER_COMPANY):
            companies.append(Company(name=f"company-{c}"))
        Company.objects.bulk_create(companies)

    def __create_positions(self):
        positions = []
        for p in self.POSITIONS:
            positions.append(Position.objects.create(name=p))
        return positions

    def __create_locations(self):
        locations = []
        for l in self.LOCATIONS:
            locations.append(Location.objects.create(name=l))
        return locations

    def __create_departments_and_dynamic_columns(self):
        departments = []
        dynamic_columns = []
        for company in Company.objects.all().order_by("-id"):
            for d in range(self.NUMBER_DEPARTMENT):
                departments.append(Department(name=random.choice(self.DEPARTMENTS), company=company))
            dynamic_columns.append(
                DynamicColumn(company=company, fields=",".join(random.sample(self.EXIST_FIELDS, 3)))
            )
        Department.objects.bulk_create(departments)
        DynamicColumn.objects.bulk_create(dynamic_columns)

    def handle(self, *args, **options):
        self.__create_companies()
        postions = self.__create_positions()
        locations = self.__create_locations()
        self.__create_departments_and_dynamic_columns()

        employees = []
        for department in Department.objects.all().order_by("-id"):
            for e in range(self.NUMBER_EMPLOYEE):
                employees.append(
                    Employee(
                        company=department.company,
                        department=department,
                        first_name=f"first_name-{e}",
                        last_name=f"last_name-{e}",
                        contact_info=f"{department.id}-{e}",
                        location=random.choice(locations),
                        position=random.choice(postions),
                        status=random.choice(
                            [Employee.ACTIVE, Employee.NOT_STARTED, Employee.TERMINATED]
                        ),
                    )
                )

        Employee.objects.bulk_create(employees, batch_size=30000)

        # create one department manager for the company 99
        department_manager_company_99 = User.objects.create_user(
            username="department_manager_company_99",
            password="1234",
        )
        Employee.objects.create(
            company=department.company,
            department=department,
            first_name=f"first_name-{e}-admin",
            last_name=f"last_name-{e}-admin",
            contact_info=f"{department.id}-{e}",
            location=random.choice(locations),
            position=Position.objects.get(name="manager"),
            status=Employee.ACTIVE,
            auth_user=department_manager_company_99,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Created department manager for {department.company}")
        )

        self.stdout.write(
            self.style.SUCCESS("=========== finished command =======================")
        )
