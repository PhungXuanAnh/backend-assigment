from django.core.cache import cache
from rest_framework import views
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from employee.models import Employee, DynamicColumn
from employee.serializers import EmployeeSerializer, QueryParamsSerializer
from main.pagination import CustomizedPagination
from main.permission import ListEmployeePermission


class EmployeeListAPIView(CustomizedPagination, views.APIView):
    permission_classes = [ListEmployeePermission]

    def get_queryset(self, query: QueryParamsSerializer, user):
        if company := query.get("company"):
            queryset = Employee.objects.filter(company__name=company)
        elif user.is_superuser:
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.none()

        if status := query.get("status"):
            queryset = queryset.filter(status__in=status)
        if location := query.get("location"):
            queryset = queryset.filter(location__name=location)
        if department := query.get("department"):
            queryset = queryset.filter(department__name=department)
        if position := query.get("position"):
            queryset = queryset.filter(position__name=position)

        return queryset.order_by("-id").order_by("-id").select_related(
            "company", "department", "position",
            "location"
        )

    def get_dynamic_fields(self, company):
        all_fields = list(EmployeeSerializer().get_fields().keys())
        if not company:
            return all_fields

        cached_fields = cache.get(company)
        if cached_fields:
            return cached_fields.split(",")

        dynamic_column = DynamicColumn.objects.filter(company__name=company).first()
        if not dynamic_column:
            dynamic_column_cfg = all_fields
        else:
            dynamic_column_cfg = dynamic_column.fields.split(",")
        cache.set(company, ",".join(dynamic_column_cfg))
        return dynamic_column_cfg

    @swagger_auto_schema(
        query_serializer=QueryParamsSerializer,
        responses={
            200: openapi.Response(
                "List Employee API Response",
                CustomizedPagination.response_serializer(EmployeeSerializer()),
            )
        },
        operation_description="Response of List Employee API",
    )
    def get(self, request, *args, **kwargs):
        query_serializer = QueryParamsSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query = query_serializer.validated_data
        qs = self.get_queryset(query, request.user)
        page = self.paginate_queryset(qs, request)
        return Response(
            self.get_paginated_response_data(
                EmployeeSerializer(
                    page,
                    many=True,
                    fields=self.get_dynamic_fields(query.get("company")),
                ).data
            )
        )
