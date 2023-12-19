from typing import Optional
from fastapi.params import Query
from fastapi import HTTPException
from pydantic import BaseModel, RootModel, ConfigDict


class ListEmployeeQueryParams(object):
    def __init__(
        self,
        company: str = Query(
            None,
            description="filter by company",
            max_length=20,
        ),
        location: str = Query(
            None,
            description="filter by location",
            max_length=20,
        ),
        department: str = Query(
            None,
            description="filter by department",
            max_length=20,
        ),
        position: str = Query(
            None,
            description="filter by position",
            max_length=20,
        ),
        status: list[str] = Query(
            [],
            description="Filter by status. Already status: `active`, `not_started`, `block_name`",
        ),
        limit: int = Query(
            10,
            ge=1,
            le=100,
            description="Page size",
        ),
        offset: int = Query(
            0,
            ge=0,
            description="Get data from",
        ),
    ):
        self.validate_status(status)
        self.company = company
        self.location = location
        self.department = department
        self.position = position
        self.status = status
        self.limit = limit
        self.offset = offset

    def validate_status(self, status):
        for s in status:
            if s not in ["active", "not_started", "block_name"]:
                details = f"Unknown status {s}. Choose in existing status: active, not_started, block_name"
                raise HTTPException(status_code=400, detail=details)


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class Department(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    # company: Company


class Location(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class Position(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class EmployeeSerializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: Optional[str]
    last_name: Optional[str]
    contact_info: Optional[str]
    status: Optional[str]

    location: Optional[Location]
    company: Optional[Company]
    department: Optional[Department]
    position: Optional[Position]


class EmployeeListSerializer(RootModel):
    root: list[EmployeeSerializer]
    model_config = ConfigDict(from_attributes=True)


class PageSerializer(BaseModel):
    items: list[EmployeeSerializer] = []
    limit: int
    offset: int
    total: int
