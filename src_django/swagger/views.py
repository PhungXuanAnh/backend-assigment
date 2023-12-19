# pylint: disable=line-too-long
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    """
    This class for using both HTTP and Https in swagger
    reference: https://stackoverflow.com/a/68021739/7639845

    Another way is using url as comment bellow
    """

    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


SwaggerView = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version="v1",
        description="This is API docs for backend assignment",
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=(permissions.AllowAny,),
    # authentication_classes=(SessionAuthentication,),    # NOTE: allow authenticate user to call api after login from admin page
)
