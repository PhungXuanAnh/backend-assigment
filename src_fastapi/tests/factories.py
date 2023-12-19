import factory
from factory.fuzzy import FuzzyText
from factory.alchemy import SQLAlchemyModelFactory
from database.models import DynamicColumn, Employee, Company, Location, Position, Department
from database.db_connection import Session


class CompanyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Company
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()


class DepartmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Department
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()
    company = CompanyFactory


class PositionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Position
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()


class LocationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()


class CompanyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Company
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText()


class EmployeeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Employee
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    first_name = FuzzyText()
    last_name = FuzzyText()
    contact_info = FuzzyText()
    status = FuzzyText()



class DynamicColumnFactory(SQLAlchemyModelFactory):
    class Meta:
        model = DynamicColumn
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    fields = FuzzyText()
