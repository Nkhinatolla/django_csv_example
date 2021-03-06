from django.core.files.base import ContentFile

from fakecsv.models import Schema, Column, Dataset
from fakecsv.utils import (get_full_name, get_random_name, get_phone_number, get_integer,
                           get_email, get_job, get_domain, get_company, get_text, get_address)


def perform_columns_to_schema(schema: Schema, columns):
    for column in columns:
        action = column.pop('action')
        if action == Column.Action.ADD:
            column_instance = Column(schema_id=schema.id, **column)
            column_instance.save()
            schema.column_set.add(column_instance)
        else:
            column_id = column.pop('id')
            if action == Column.Action.UPDATE:
                Column.objects.filter(id=column_id).update(**column)
            if action == Column.Action.DELETE:
                Column.objects.get(id=column_id).delete()

    return Schema.objects.get(id=schema.id)


def get_fake_data(column, string_char, column_separator):
    if column['type'] == Column.Type.FULL_NAME:
        data = get_full_name().replace(column_separator, "")
    elif column['type'] == Column.Type.EMAIL:
        data = get_email().replace(column_separator, "")
    elif column['type'] == Column.Type.JOB:
        data = get_job().replace(column_separator, "")
    elif column['type'] == Column.Type.DOMAIN_NAME:
        data = get_domain().replace(column_separator, "")
    elif column['type'] == Column.Type.COMPANY_NAME:
        data = get_company().replace(column_separator, "")
    elif column['type'] == Column.Type.ADDRESS:
        data = get_address().replace(column_separator, "")
    elif column['type'] == Column.Type.TEXT:
        data = get_text().replace(column_separator, "")
    elif column['type'] == Column.Type.PHONE_NUMBER:
        data = get_phone_number().replace(column_separator, "")
    elif column['type'] == Column.Type.INTEGER:
        data = get_integer(int(column['extra_data']['start_range']), int(column['extra_data']['end_range']))
        return data
    else:
        data = get_random_name(10)
    return string_char + data + string_char


def generate_dataset(dataset: Dataset):
    column_separator = dataset.schema.column_separator
    string_char = dataset.schema.string_character
    result = f"{column_separator}".join(list(dataset.schema.column_set.values_list('name', flat=True))) + '\n'
    for row_id in range(dataset.rows):
        row = []
        for column in dataset.schema.column_set.values('type', 'extra_data'):
            data = get_fake_data(column, string_char, column_separator)
            row.append(data)
        result += f"{column_separator}".join(row) + '\n'
    content = ContentFile(result.encode('ascii'))
    dataset.result_file.save(Dataset.result_file.field.upload_to(dataset, ""), content)
    dataset.status = Dataset.Status.READY
    dataset.save()


# def download_dataset(instance: Dataset):
#     file_path = instance.result_file.path
#     with open(file_path, 'rb') as fh:
#         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#         return response
