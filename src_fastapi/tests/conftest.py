import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import close_all_sessions

from base64 import b64encode

current_dir = Path(__file__).resolve(strict=True).parent
sys.path.append(str(current_dir.parent))

from database.models import Employee, Base
from controller.utilities import get_connection_string
from main import app
from tests.factories import (
    EmployeeFactory,
    DynamicColumnFactory,
    CompanyFactory,
    DepartmentFactory,
    LocationFactory,
    PositionFactory,
)


@pytest.fixture(scope="function", autouse=True)
def reset_database_test():
    """
    scope is function mean that reset database for each test function
    reference: https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
    """
    engine = create_engine(get_connection_string())
    conn = engine.connect()
    Base.metadata.create_all(bind=engine)
    yield
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)
    conn.close()
    engine.dispose()


@pytest.fixture(scope="module")
def anonymous_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def department_manager_client():
    username = "department_manager_company_99"
    password = "1234"
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return TestClient(app, headers={"Authorization": f"Basic {token}"})


@pytest.fixture(scope="module")
def superuser_client():
    username = "admin"
    password = "admin"
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return TestClient(app, headers={"Authorization": f"Basic {token}"})


@pytest.fixture
def test_data():
    fields = "department,position,location"
    company = CompanyFactory(name="company-99")
    location = LocationFactory()
    position_manager = PositionFactory(name="manager")
    position_staff = PositionFactory(name="staff")

    DynamicColumnFactory(company=company, fields=fields)

    # create 1 department manager employee for current company
    department = DepartmentFactory(company=company)
    department_manager_employee = EmployeeFactory(
        company=company,
        department=department,
        location=location,
        position=position_manager
        # auth_user=department_manager,
    )

    # create 5 employee of the current company
    NUMBER_EMPLOYEES_OFF_CURRENT_COMPANY = 5
    for i in range(NUMBER_EMPLOYEES_OFF_CURRENT_COMPANY):
        EmployeeFactory(
            company=company,
            department=department,
            location=location,
            position=position_staff,
        )

    # create 5 employee of the other company
    another_company = CompanyFactory(name="another-company")
    NUMBER_EMPLOYEES_OFF_ANOTHER_COMPANY = 5
    for i in range(NUMBER_EMPLOYEES_OFF_ANOTHER_COMPANY):
        EmployeeFactory(
            company=another_company,
            department=department,
            location=location,
            position=position_staff,
        )
    return {
        "department_manager_employee": department_manager_employee,
        "total_employees_in_current_company": NUMBER_EMPLOYEES_OFF_CURRENT_COMPANY
        + 1,  # one more department manager
        "total_employees_in_another_company": NUMBER_EMPLOYEES_OFF_ANOTHER_COMPANY,
        "total_employees": NUMBER_EMPLOYEES_OFF_CURRENT_COMPANY
        + NUMBER_EMPLOYEES_OFF_ANOTHER_COMPANY
        + 1,
    }
