from rest_framework import serializers
from employee.models import Employee


class CommaSeparatedField(serializers.CharField):
    """Comma-separated field"""

    def __init__(self, **kwargs):
        kwargs.setdefault("help_text", "Comma-separated list of values.")
        kwargs.setdefault("allow_blank", True)
        self.ignore_blank_element = kwargs.pop("ignore_blank_element", True)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        s = super().to_internal_value(data)
        if isinstance(s, str):
            v_list = [v.strip() for v in data.split(",")]
            if self.ignore_blank_element:
                v_list = [v for v in v_list if v]
        else:
            v_list = []
        return v_list


class QueryParamsSerializer(serializers.Serializer):
    company = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    department = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    status = CommaSeparatedField(
        required=False,
        allow_blank=True,
        help_text=(
            "Comma-separated list of values. "
            f"Possible values: {', '.join([f'`{v}`' for v in [Employee.ACTIVE, Employee.NOT_STARTED, Employee.TERMINATED]])}"
        ),
    )


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        default_fields = {"status", "first_name", "last_name"}

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed - default_fields:
                self.fields.pop(field_name)


class EmployeeSerializer(DynamicFieldsModelSerializer):
    company = serializers.ReadOnlyField(source="company.name")
    location = serializers.ReadOnlyField(source="location.name")
    position = serializers.ReadOnlyField(source="position.name")
    department = serializers.ReadOnlyField(source="department.name")

    class Meta:
        model = Employee
        fields = "__all__"
