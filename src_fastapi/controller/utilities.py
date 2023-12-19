import os
from typing import Any
import redis as python_redis

from controller.schema import EmployeeSerializer


class TransformerDynamicColumn(object):
    def __init__(self, redis_url) -> None:
        self.redis = python_redis.from_url(redis_url)
        self.all_fields = list(EmployeeSerializer.model_fields.keys())

    def get_dynamic_columns(self, company):
        # import here to avoid circular import
        from database.repository import DynamicColumnRepository
        
        if not company:
            return self.all_fields

        cached_dynamic_columns = self.redis.get(company)
        if cached_dynamic_columns and os.environ.get("ENVIRONMENT") != "pytest":
            return cached_dynamic_columns.decode("utf-8").split(",")

        dynamic_columns = DynamicColumnRepository().get_dynamic_column(company)
        if dynamic_columns and dynamic_columns.fields:
            dynamic_columns_cfg = dynamic_columns.fields.split(",")
        else:
            dynamic_columns_cfg = self.all_fields

        self.redis.set(company, ",".join(dynamic_columns_cfg))
        return dynamic_columns_cfg

    def __call__(self, items, company) -> Any:
        dynamic_columns = self.get_dynamic_columns(company)
        default_fields = {"status", "first_name", "last_name"}
        existing = set(self.all_fields)
        allowed = set(dynamic_columns)
        for item in items:
            for field_name in existing - allowed - default_fields:
                item.pop(field_name)
        return items


def get_connection_string():
    env = os.environ.get("ENVIRONMENT")
    if env == "pytest":
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            user=os.environ.get("POSTGRES_USER", "root"),
            password=os.environ.get("POSTGRES_PASSWORD", "1234_password"),
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=os.environ.get("POSTGRES_PORT", 5432),
            db="test_db",
        )
    elif env == "local":
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            user=os.environ.get("POSTGRES_USER", "root"),
            password=os.environ.get("POSTGRES_PASSWORD", "1234_password"),
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=os.environ.get("POSTGRES_PORT", 5432),
            db=os.environ.get("POSTGRES_DB", "omni_hr_db"),
        )
    else:
        raise Exception(
            "Don't know current working environment, please set environment variable ENVIRONMENT"
        )
