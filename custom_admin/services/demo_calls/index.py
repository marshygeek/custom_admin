import requests

from custom_admin.services.utils import wrap_request_method, handle_request_errors
from custom_admin.config import CORE_API_V1, CORE_DEMO_API
from custom_admin.services.demo_calls.structures import CachedObject

# it's about 1 hour
CACHE_TIME = 3600

cities_cache = CachedObject()

integrations_cache = CachedObject()


def pull_cities(use_cache=True):
    if use_cache:
        if cities_cache.get_downtime() > CACHE_TIME:
            response = get_cities_from_platform()

            if 'error_message' in response:
                return response

            cities_cache.update_value(response)

        result = cities_cache.get_value()
    else:
        result = get_cities_from_platform()

    return result


def construct_city(city_info):
    return {
        'id': int(city_info['id']),
        'name': city_info['name'],
        'longitude': float(city_info['longitude']),
        'latitude': float(city_info['latitude']),
    }


def get_cities_from_platform():
    url = CORE_API_V1.format("cities")
    request_method = wrap_request_method(requests.get, url)

    content = handle_request_errors(request_method, 'get cities list')
    if 'error_message' in content:
        return content

    cities = [construct_city(city) for city in content['result']]
    return cities


def pull_integrations(use_cache=True):
    if use_cache:
        if integrations_cache.get_downtime() > CACHE_TIME:
            response = get_integrations_from_platform()

            if 'error_message' in response:
                return response

            integrations_cache.update_value(response)

        result = integrations_cache.get_value()
    else:
        result = get_integrations_from_platform()

    return result


def construct_integration(integration_info):
    return {
        'id': int(integration_info['id']),
        'city_id': int(integration_info['city_id']),
        'sip_prefix': integration_info['sip'],
    }


def get_integrations_from_platform():
    url = CORE_DEMO_API.format('integrations')
    request_method = wrap_request_method(requests.get, url)

    content = handle_request_errors(request_method, 'get integrations list')
    if 'error_message' in content:
        return content

    integrations = [construct_integration(integration) for integration in content['result']]
    return integrations
