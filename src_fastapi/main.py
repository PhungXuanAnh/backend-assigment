import os
import json
from typing import Any
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from controller.schema import (
    ListEmployeeQueryParams,
    PageSerializer,
    EmployeeListSerializer,
)
from database.repository import EmployeeRepository, DynamicColumnRepository
from controller.rate_limiter import RateLimiter
from controller.utilities import TransformerDynamicColumn
from controller.auth import get_auth_user

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = RateLimiter(
    redis_url="redis://{redis_host}:{redis_port}/{redis_db}".format(
        redis_host=os.environ.get("REDIS_HOST", "localhost"),
        redis_port=os.environ.get("REDIS_PORT", 6379),
        redis_db=os.environ.get("REDIS_DB", 7),
    ),
    times=2,
    period_second=10,  # it mean the user can only call 2 requests every 10 seconds
)


transformer_dynamic_column = TransformerDynamicColumn(
    redis_url="redis://{redis_host}:{redis_port}/{redis_db}".format(
        redis_host=os.environ.get("REDIS_HOST", "localhost"),
        redis_port=os.environ.get("REDIS_PORT", 6379),
        redis_db=os.environ.get("REDIS_DB", 8),
    ),
)


@app.get(
    "/",
    response_model=PageSerializer,
    status_code=200,
    response_model_exclude_none=True,
)
async def list_employee(
    query_params: ListEmployeeQueryParams = Depends(),
    _: Any = Depends(rate_limiter),
    auth_user: str = Depends(get_auth_user),
):
    """Get list of employee"""

    if not auth_user["is_superuser"] and auth_user["company"] != query_params.company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't specify your company or you don't have permission to list employees of the specified company",
        )
    employees = EmployeeRepository().filter_employees(query_params)
    paginated_employees = employees.limit(query_params.limit).offset(query_params.offset)
    items = EmployeeListSerializer.model_validate(paginated_employees).model_dump()
    final_items = transformer_dynamic_column(items, query_params.company)

    response = {
        "items": final_items,
        "limit": query_params.limit,
        "offset": query_params.offset,
        "total": employees.count(),
    }
    return Response(content=json.dumps(response), media_type="application/json")
