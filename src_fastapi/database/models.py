from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import MetaData, Column, String, Integer, ForeignKey

metadata = MetaData()
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee_employee"

    id = Column(Integer, primary_key=True)
    first_name = Column("first_name", String, nullable=True)
    last_name = Column("last_name", String, nullable=True)
    contact_info = Column("contact_info", String, nullable=True)
    status = Column("status", String, nullable=True)

    department_id = Column(Integer, ForeignKey("employee_department.id"))
    position_id = Column(Integer, ForeignKey("employee_position.id"))
    location_id = Column(Integer, ForeignKey("employee_location.id"))
    company_id = Column(Integer, ForeignKey("employee_company.id"))

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    location = relationship("Location", back_populates="employees")
    company = relationship("Company", back_populates="employees")


class Company(Base):
    __tablename__ = "employee_company"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    dynamic_columns = relationship("DynamicColumn", back_populates="company")
    employees = relationship("Employee", back_populates="company")
    departments = relationship("Department", back_populates="company")


class DynamicColumn(Base):
    __tablename__ = "employee_dynamiccolumn"

    id = Column(Integer, primary_key=True)
    fields = Column("fields", String, nullable=True)
    company_id = Column(Integer, ForeignKey("employee_company.id"))

    company = relationship("Company", back_populates="dynamic_columns")


class Location(Base):
    __tablename__ = "employee_location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="location")


class Position(Base):
    __tablename__ = "employee_position"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="position")


class Department(Base):
    __tablename__ = "employee_department"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    company_id = Column(Integer, ForeignKey("employee_company.id"))

    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department")
