from custom_admin.services.demo_calls.index import pull_cities, pull_integrations


def get_cities_list():
    cities = pull_cities()
    if 'error_message' in str(cities):
        return cities

    integrations = pull_integrations()
    if 'error_message' in str(cities):
        return integrations

    supported_cities = [integration['city_id'] for integration in integrations]
    return [city for city in cities if city['id'] in supported_cities]
