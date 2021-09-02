from celery import shared_task
from fakecsv.models import Dataset
from fakecsv import services


@shared_task(name="example_csv.generate_task", default_retry_delay=10, max_retries=3)
def generate_task(dataset_id):
    try:
        dataset = Dataset.objects.select_related('schema').prefetch_related('schema__column_set').get(id=dataset_id)
        services.generate_dataset(dataset)
    except Exception as e:
        raise generate_task.retry(exc=e)
