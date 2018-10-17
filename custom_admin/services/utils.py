from datetime import datetime
from json import JSONDecodeError, load, dumps

import requests

from custom_admin.config import *


def wrap_request_method(request_method, *args, **kwargs):
    def _wrapper():
        return request_method(*args, **kwargs)

    return _wrapper


def handle_request_errors(request_method, request_name):
    try:
        response = request_method()

        try:
            content = response.json()
            if check_not_failed(response.status_code, content):
                return content
            else:
                errors = content
        except JSONDecodeError:
            errors = response.text
    except requests.ConnectionError as err:
        errors = str(err)

    result = {
        'error_message': 'failed to {}'.format(request_name),
        'response': errors,
    }
    logger.error(result)
    return result


def check_not_failed(status, content):
    error_field_names = ['error', 'errors', 'error_list']
    for field in error_field_names:
        if field in content:
            return False

    return status == 200


def extract_mock_file(filename, prefix=''):
    with open(join(MOCK_FILES_DIR, join(prefix, filename) + '.json'), encoding='utf8') as file:
        return load(file)


def extract_template(filename, prefix=''):
    with open(join(SERVICES_TEMPLATES_DIR, join(prefix, filename) + '.html'), encoding='utf8') as file:
        return file.read()


def pretty_dumps(value):
    return dumps(value, indent=2, ensure_ascii=False)


def to_normal_time(utc_time, using_ms=True):
    divider = 1e3 if using_ms else 1
    utc_time = datetime.fromtimestamp(utc_time / divider)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # trimming microseconds by 3 points
