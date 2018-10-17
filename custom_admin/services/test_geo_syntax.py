import requests

from custom_admin.services.utils import wrap_request_method, handle_request_errors
from custom_admin.config import SYNTAX_API, GEO_API


def get_test_service_params(city_id, query_text):
    params = {}

    result = request_tagging(city_id, query_text)
    params['tags'] = result

    if 'error_message' not in result:
        locations = []
        for tag in result:
            location = request_location(tag['tag_info']['city_id'], tag['tag'])
            locations.append(location)
        params['locations'] = locations

    return params


def request_tagging(city_id, query_text):
    url = SYNTAX_API.format('tagging')
    request_method = wrap_request_method(requests.post, url, json={
        'text': query_text,
        'tag_types': [{
            "tag_type": "geo",
            "city_id": city_id
        }],
    })

    content = handle_request_errors(request_method, 'request tagging')
    if 'error_message' in content:
        return content

    return content['result']


def request_location(city_id, tag):
    url = GEO_API.format('location')
    request_method = wrap_request_method(requests.post, url, json={
        "city": city_id,
        "tag": tag,
    })

    content = handle_request_errors(request_method, 'request location')
    if 'error_message' in content:
        return content

    return content['result']
