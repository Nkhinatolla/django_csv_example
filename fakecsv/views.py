import os

from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from fakecsv import serializers
from fakecsv.models import Schema, Column, Dataset
from fakecsv import services
from csv_example import celery_app


class SchemaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Schema.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SchemaListSerializer
        return serializers.SchemaDetailSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        column_set = serializer.validated_data.pop('column_set')
        instance = self.perform_create(serializer)
        instance = services.perform_columns_to_schema(instance, column_set)
        serializer = serializers.SchemaDetailSerializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        column_set = serializer.validated_data.pop('column_set')
        self.perform_update(serializer)
        instance = services.perform_columns_to_schema(instance, column_set)
        serializer = serializers.SchemaDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], name='Get field choices to representation')
    def choices(self, request, *args, **kwargs):
        response = {
            "schema": [
                {
                    "field": "column_separator",
                    "choices": Schema.SeparatorSymbol.choices
                },
                {
                    "field": "string_character",
                    "choices": Schema.StringChar.choices
                },
            ],
            "column": [
                {
                    "field": "type",
                    "choices": Column.Type.choices,
                },
                {
                    "field": "action",
                    "choices": Column.Action.choices,
                },
            ]
        }
        return Response(response)


class DatasetViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DatasetListSerializer
    queryset = Dataset.objects.none()

    def get_queryset(self):
        return Dataset.objects.filter(schema_id=self.kwargs['schema_id'])

    def perform_create(self, serializer):
        instance = serializer.save()
        celery_app.send_task(name='example_csv.generate_task', kwargs={'dataset_id': instance.id}, queue='csv_example')



