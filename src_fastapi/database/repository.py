from database.db_connection import Session
from controller.schema import ListEmployeeQueryParams
from database.models import Employee, DynamicColumn
from sqlalchemy import and_, desc


class BaseRepository:
    def __init__(self):
        self.db = Session()


class EmployeeRepository(BaseRepository):
    def filter_employees(self, params: ListEmployeeQueryParams):
        conditions = []

        if params.company:
            conditions.append(Employee.company.has(name=params.company))

        if params.location:
            conditions.append(Employee.location.has(name=params.location))

        if params.department:
            conditions.append(Employee.department.has(name=params.department))

        if params.position:
            conditions.append(Employee.position.has(name=params.position))

        if params.status:
            conditions.append(Employee.status.in_(params.status))

        query = self.db.query(Employee).filter(and_(True, *conditions)).order_by(desc("id"))
        return query


class DynamicColumnRepository(BaseRepository):
    def get_dynamic_column(self, company):
        return self.db.query(DynamicColumn).filter(DynamicColumn.company.has(name=company)).first()
