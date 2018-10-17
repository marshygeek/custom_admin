from urllib.parse import quote

import requests

from al_admin.settings import STATIC_URL
from custom_admin.config import DIALOG_API
from custom_admin.services.utils import wrap_request_method, handle_request_errors


def get_tts_filename(phrase, from_cache=False):
    suffix = 'tts/phrase/{}'.format(quote(phrase))
    if from_cache:
        suffix += '/cache'

    url = DIALOG_API.format(suffix)
    request_method = wrap_request_method(requests.get, url)

    content = handle_request_errors(request_method, 'get tts filename')
    if 'error_message' in content:
        return content

    return content['result']


def get_tts_generation_params(query_text):
    result = get_tts_filename(query_text)
    if 'error_message' not in result:
        result = f'{STATIC_URL}{result[1:]}'

    return {'tts_filename': result}
