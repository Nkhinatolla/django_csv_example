from django.contrib import admin
from fakecsv.models import Schema, Column, Dataset


class ColumnTabularInline(admin.TabularInline):
    model = Column


@admin.register(Schema)
class SchemaModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modified')
    inlines = (ColumnTabularInline, )


@admin.register(Dataset)
class DatasetModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'schema', 'created', 'status', 'result_file')
