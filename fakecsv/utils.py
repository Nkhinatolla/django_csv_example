import string
import random
from faker import Faker

fake = Faker()


def get_integer(start_range, end_range):
    return str(random.randint(start_range, end_range))


def get_phone_number(n=11):
    return fake.phone_number()


def get_full_name():
    return fake.name()


def get_email():
    return fake.email()


def get_job():
    return fake.job()


def get_domain():
    return fake.domain_name()


def get_company():
    return fake.company()


def get_text():
    return fake.text()


def get_address():
    return fake.address()


def get_random_name(length=25):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def dataset_upload(instance, filename):
    return 'dataset/{}.{}'.format(get_random_name(), 'csv')
