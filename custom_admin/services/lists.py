from unittest.mock import patch

import requests
from django.urls import reverse

from al_admin.settings import STATIC_URL
from custom_admin.config import *
from custom_admin.services.utils import wrap_request_method, handle_request_errors, to_normal_time, extract_mock_file
from custom_admin.tests import static_paginator


def parse_page_num(get_params, total_pages):
    number = get_params.get('page')
    try:
        number = int(number)
    except (TypeError, ValueError):
        number = 1

    if number < 1 or number > total_pages:
        number = 1

    return number


def get_paginator(token, get_params, filter_params, list_name):
    suffix = '{}/count'.format(list_name)
    url = CORE_API_CP1.format(suffix)

    payload = {'access_token': token}
    payload.update(filter_params)

    request_method = wrap_request_method(requests.get, url, params=payload)

    content = handle_request_errors(request_method, 'get {} count'.format(list_name))
    if 'error_message' in content:
        return content

    items_count = int(content['result'])

    per_page = PAGINATOR_PER_PAGE
    total_pages = ((items_count + per_page) - 1) // per_page

    page_num = parse_page_num(get_params, total_pages)

    return {
        'has_previous': page_num > 1,
        'previous_page_number': page_num - 1,
        'number': page_num,
        'has_next': page_num < total_pages,
        'next_page_number': page_num + 1,
        'num_pages': total_pages
    }


def get_ordering_params(get_params, col_names):
    order_params = {}
    if 'ordering' in get_params:
        sort_param = get_params['ordering']

        if '-' in sort_param:
            sort_param = sort_param[1:]
            direction = 'DESC'
        else:
            direction = 'ASC'

        if sort_param in col_names:
            order_params['order_by_filed'] = sort_param
            order_params['order_by_direction'] = direction

    return order_params


def get_list_params(token, get_params, list_name):
    col_names = {
        'partners': SHORT_PARTNER_COLS,
        'integrations': SHORT_INTEGRATION_COLS,
        'calls': SHORT_CALL_COLS,
        'webhooks': SHORT_WEBHOOK_COLS,
        'orders': SHORT_ORDER_COLS,
    }[list_name]

    # getting parameters for filtering
    filter_params = {col_name: get_params[col_name] for col_name in col_names
                     if col_name in get_params and get_params[col_name] != ''}

    paginator = get_paginator(token, get_params, filter_params, list_name)
    if 'error_message' in paginator:
        return paginator

    order_params = get_ordering_params(get_params, col_names)

    item_list = get_list(token, list_name, paginator['number'], filter_params, order_params)
    if 'error_message' in item_list:
        return item_list

    urls = {
        'id': '{list_url}{id}/'.format(list_url=reverse('custom_admin:{}'.format(list_name)), id='{}')
    }

    rows = [{col_name: item[col_name] for col_name in col_names} for item in item_list]

    apply_display_changes(rows)

    return {
        'urls': urls,
        'col_names': col_names,
        'rows': rows,
        'paginator': paginator
    }


def apply_display_changes(rows):
    for row in rows:
        for col_name in ('ctime', 'utime'):
            if col_name in row:
                row[col_name] = to_normal_time(row[col_name], using_ms=False)


def get_list(token, list_name, page_num, filter_params, order_params):
    url = CORE_API_CP1.format(list_name)
    if 'integration_id' in filter_params:
        url += '/integration/{}'.format(filter_params['integration_id'])
    elif 'partner_id' in filter_params:
        url += '/partner/{}'.format(filter_params['partner_id'])

    payload = {
        'access_token': token,
        'limit': PAGINATOR_PER_PAGE,
        'offset': PAGINATOR_PER_PAGE * (page_num - 1)
    }
    payload.update(order_params)
    request_method = wrap_request_method(requests.get, url, params=payload)

    content = handle_request_errors(request_method, 'get {}'.format(list_name))
    if 'error_message' in content:
        return content

    return content['result']


def get_partners_transit_btn():
    btn_html = '<a href="{url}?transit=1&partner_id={id}" style="display:inline;" class="btn btn-sm">Интеграции</a>' \
        .format(url=reverse('custom_admin:integrations'), id='{}')
    return btn_html


def get_partners_params(token, get_params):
    list_name = 'partners'

    partners_params = get_list_params(token, get_params, list_name)
    if 'error_message' in partners_params:
        return partners_params

    partners_params['can_edit'] = True
    partners_params['transit_btn'] = get_partners_transit_btn()

    return partners_params


def get_integrations_transit_btn(partner_id=None):
    partner_param = '&partner_id={}'.format(partner_id) if partner_id else ''
    href = '{url}?transit=1{partner_param}&integration_id={integ_id}' \
        .format(url=reverse('custom_admin:calls'), partner_param=partner_param, integ_id='{}')
    btn_html = '<a href="{}" style="display:inline;" class="btn btn-sm">Звонки</a>'.format(href)
    return btn_html


def get_integrations_params(token, get_params):
    list_name = 'integrations'

    integrations_params = get_list_params(token, get_params, list_name)
    if 'error_message' in integrations_params:
        return integrations_params

    integrations_params['can_edit'] = True

    partner_id = get_params.get('partner_id')
    integrations_params['transit_btn'] = get_integrations_transit_btn(partner_id)
    if get_params.get('transit'):
        integrations_params['prev_links'] = {
            'partners': reverse('custom_admin:partners'),
            'integrations': '#'
        }

    return integrations_params


def get_calls_params(token, get_params):
    list_name = 'calls'

    get_params = {key: val for key, val in get_params.items()}

    if 'ordering' not in get_params:
        get_params['ordering'] = '-id'

    calls_params = get_list_params(token, get_params, list_name)
    if 'error_message' in calls_params:
        return calls_params

    calls_params['can_edit'] = False

    calls_params['additional_col'] = {
        'name': 'Запись звонка',
        'required_field': 'record',
        'template': """
            <audio controls>
              <source src="{static_url}tmp/dialog/call_records/{filename}" type="audio/wav">
              Your browser does not support the audio element.
            </audio>
        """.format(static_url=STATIC_URL, filename='{}')
    }

    if get_params.get('transit'):
        integrations_url = reverse('custom_admin:integrations')

        partner_id = get_params.get('partner_id')
        if partner_id:
            integrations_url += '?transit=1&partner_id={}'.format(partner_id)

        calls_params['prev_links'] = {
            'partners': reverse('custom_admin:partners'),
            'integrations': integrations_url,
            'calls': '#',
        }

    return calls_params


def get_webhooks_params(token, get_params):
    list_name = 'webhooks'

    with patch('custom_admin.services.lists.get_paginator') as paginator:
        paginator.return_value = static_paginator

        with patch('custom_admin.services.lists.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: extract_mock_file('list', list_name[:-1])
            mocked_get.return_value.status_code = 200

            webhooks_params = get_list_params(token, get_params, list_name)
            if 'error_message' in webhooks_params:
                return webhooks_params

            webhooks_params['can_edit'] = True

            return webhooks_params


def get_orders_params(token, get_params):
    list_name = 'orders'

    with patch('custom_admin.services.lists.get_paginator') as paginator:
        paginator.return_value = static_paginator

        with patch('custom_admin.services.lists.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: extract_mock_file('list', list_name[:-1])
            mocked_get.return_value.status_code = 200

            orders_params = get_list_params(token, get_params, list_name)
            if 'error_message' in orders_params:
                return orders_params

            orders_params['can_edit'] = True

            return orders_params
