from unittest.mock import patch

import requests

from custom_admin.config import CORE_API_CP1
from custom_admin.services.utils import wrap_request_method, handle_request_errors, extract_mock_file


def pre_process_params(fields, params):
    return {field: params[field] for field in fields if params.get(field, '') != ''}


def change_partner(token, partner_id, params):
    fields = ['login', 'password', 'name', 'organization', 'address', 'contact_phones', 'description', 'emails']

    url = CORE_API_CP1.format('partners/{}'.format(partner_id))
    request_method = wrap_request_method(requests.put, url, json={
        'access_token': token,
        **pre_process_params(fields, params)
    })

    content = handle_request_errors(request_method, 'change partner')
    if 'error_message' in content:
        return content

    return content['result']


def change_integration(token, integration_id, params):
    fields = ['city_id', 'phone_number', 'sip', 'redirect_to_operator_sip']

    url = CORE_API_CP1.format('integrations/{}'.format(integration_id))
    request_method = wrap_request_method(requests.put, url, json={
        'access_token': token,
        **pre_process_params(fields, params)
    })

    content = handle_request_errors(request_method, 'change integration')
    if 'error_message' in content:
        return content

    return content['result']


def change_webhook(token, webhook_id, params):
    with patch('custom_admin.services.modify.requests.put') as mocked_put:
        mocked_put.return_value.json = lambda: extract_mock_file('change', 'webhook')
        mocked_put.return_value.status_code = 200

        fields = ['url', 'type', 'integration_id', 'method']

        url = CORE_API_CP1.format('webhooks/{}'.format(webhook_id))
        request_method = wrap_request_method(requests.put, url, json={
            'access_token': token,
            **pre_process_params(fields, params)
        })

        content = handle_request_errors(request_method, 'change webhook')
        if 'error_message' in content:
            return content

        return content['result']


def change_order(token, order_id, params):
    with patch('custom_admin.services.modify.requests.put') as mocked_put:
        mocked_put.return_value.json = lambda: extract_mock_file('change', 'order')
        mocked_put.return_value.status_code = 200

        fields = ['url', 'type', 'integration_id', 'method']

        url = CORE_API_CP1.format('orders/{}'.format(order_id))
        request_method = wrap_request_method(requests.put, url, json={
            'access_token': token,
            **pre_process_params(fields, params)
        })

        content = handle_request_errors(request_method, 'change order')
        if 'error_message' in content:
            return content

        return content['result']
