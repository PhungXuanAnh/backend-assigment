URL = "/"


def test_anonymous_user(anonymous_client):
    response = anonymous_client.get(URL)
    assert response.status_code == 401


def test_403_permission(department_manager_client):
    response = department_manager_client.get(URL)
    assert response.status_code == 403


def test_supersuser_list_all_employee(superuser_client, test_data):
    response = superuser_client.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == test_data["total_employees"]


def test_superuser_filter_1_company(superuser_client, test_data):
    department_manager = test_data["department_manager_employee"]
    response = superuser_client.get(URL + f"?company={department_manager.company.name}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == test_data["total_employees_in_current_company"]


def test_department_manager_filter_current_company(department_manager_client, test_data):
    department_manager = test_data["department_manager_employee"]
    response = department_manager_client.get(URL + f"?company={department_manager.company.name}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == test_data["total_employees_in_current_company"]


def test_filter_correct_data_and_correct_dynamic_column(department_manager_client, test_data):
    department_manager = test_data["department_manager_employee"]
    response = department_manager_client.get(
        URL
        + f"?company={department_manager.company.name}&department={department_manager.department.name}&position={department_manager.position.name}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1

    item = data["items"][0]
    assert item["department"]["name"] == department_manager.department.name
    assert item["position"]["name"] == department_manager.position.name
    assert item["status"] == department_manager.status
    assert item["location"]["name"] == department_manager.location.name

    assert "contact_info" not in item
