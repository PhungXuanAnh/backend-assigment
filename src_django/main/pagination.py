from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class CustomizedPagination(PageNumberPagination):
    class Serializer(serializers.Serializer):
        count = serializers.IntegerField()
        page_count = serializers.IntegerField()
        page_size = serializers.IntegerField()
        page = serializers.IntegerField()

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    @classmethod
    def request_serializer(cls, request_serializer):
        class _Serializer(request_serializer):
            class Meta:
                # for swagger
                ref_name = None

            page = serializers.IntegerField(required=False)
            page_size = serializers.IntegerField(required=False)

        return _Serializer

    @classmethod
    def response_serializer(cls, result_serializer):
        class _Serializer(cls.Serializer):
            class Meta:
                # for swagger
                ref_name = None

            results = serializers.ListSerializer(child=result_serializer, allow_empty=True)

        return _Serializer

    def get_paginated_response_data(self, data):
        return {
            "count": self.page.paginator.count,
            "page_count": self.page.paginator.num_pages,
            "page_size": self.get_page_size(self.request),
            "page": self.page.number,
            "results": data,
        }
