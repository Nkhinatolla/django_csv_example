from rest_framework import serializers
from fakecsv.models import Schema, Column, Dataset
from rest_framework.exceptions import ValidationError


class SchemaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = ('id', 'title', 'modified')


class ColumnSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=Column.Action.choices, write_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Column
        fields = ('id', 'name', 'type', 'extra_data', 'order', 'action')


class SchemaDetailSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(source='column_set', many=True)

    class Meta:
        model = Schema
        fields = ('id', 'title', 'column_separator', 'string_character', 'columns')

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        for column in self.validated_data['column_set']:
            if column['action'] == 'ADD' and 'id' in column:
                raise ValidationError(f"On column with action({column['action']}), remove 'id'")
            if column['action'] != 'ADD' and 'id' not in column:
                raise ValidationError(f"On column with action({column['action']}), add 'id'")


class DatasetListSerializer(serializers.ModelSerializer):

    rows = serializers.IntegerField(write_only=True)
    schema_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Dataset
        fields = ('id', 'created', 'status', 'rows', 'schema_id')
