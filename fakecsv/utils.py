import string
import random
import names


def get_integer(start_range, end_range):
    return str(random.randint(start_range, end_range))


def get_phone_number(n=11):
    start_range = 10 ** (n - 1)
    end_range = (10 ** n) - 1
    return f"+{random.randint(start_range, end_range)}"


def get_full_name():
    return names.get_full_name()


def get_random_name(length=25):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def dataset_upload(instance, filename):
    return 'dataset/{}.{}'.format(get_random_name(), 'csv')
