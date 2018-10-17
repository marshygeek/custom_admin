from json import loads
from unittest.mock import patch

from django.urls import reverse

from custom_admin.services.lists import get_partners_transit_btn, get_integrations_transit_btn
from custom_admin.services.parse_transcription import *
from custom_admin.services.utils import *


def get_detail_params(token, detail_name, detail_id):
    col_names = {
        'partner': FULL_PARTNER_COLS,
        'integration': FULL_INTEGRATION_COLS,
        'call': FULL_CALL_COLS,
        'webhook': FULL_WEBHOOK_COLS,
        'order': FULL_ORDER_COLS,
    }[detail_name]

    detail = get_detail(token, detail_name, detail_id)
    if 'error_message' in detail:
        return detail

    for col_name in ('ctime', 'utime'):
        if col_name in detail:
            detail[col_name] = to_normal_time(detail[col_name], using_ms=False)

    item_endpoint = reverse('custom_admin:{}'.format(detail_name), args=[detail_id])

    return {
        'item_endpoint': item_endpoint,
        'col_names': col_names,
        'detail': detail,
    }


def get_detail(token, detail_name, detail_id):
    suffix = '{name}s/{id}'.format(name=detail_name, id=detail_id)
    url = CORE_API_CP1.format(suffix)

    payload = {'access_token': token}
    request_method = wrap_request_method(requests.get, url, params=payload)

    content = handle_request_errors(request_method, 'get {}'.format(detail_name))
    if 'error_message' in content:
        return content

    return content['result']


def get_partner_params(token, partner_id):
    detail_name = 'partner'

    partner_params = get_detail_params(token, detail_name, partner_id)
    if 'error_message' in partner_params:
        return partner_params

    partner_params['can_edit'] = True
    partner_params['transit_btn'] = get_partners_transit_btn().format(partner_id)

    return partner_params


def get_integration_params(token, integration_id):
    detail_name = 'integration'

    integration_params = get_detail_params(token, detail_name, integration_id)
    if 'error_message' in integration_params:
        return integration_params

    integration_params['can_edit'] = True
    integration_params['transit_btn'] = get_integrations_transit_btn().format(integration_id)

    return integration_params


def get_call_params(token, call_id):
    detail_name = 'call'

    call_params = get_detail_params(token, detail_name, call_id)
    if 'error_message' in call_params:
        return call_params

    call_params['can_edit'] = False

    try:
        transcription = loads(call_params['detail']['transcription'])
    except JSONDecodeError:
        transcription = None
    try:
        form = loads(call_params['detail']['form'])
    except JSONDecodeError:
        form = None

    call_params['preview_block'] = get_call_preview_block(transcription, form, call_params['detail']['record'])

    return call_params


def get_call_preview_block(transcription, form, record_filename):
    preview_block = ''

    if transcription:
        detail_block = generate_detail_block(transcription['detail'])

        preview_block = '<div id="detail">{}</div>'.format(detail_block)

    if form:
        preview_block = """
            {remainder}
            <br>
            <div id="order_on_map">
                {map_block}
            </div>
        """.format(remainder=preview_block, map_block=get_map_block(form))

    if record_filename and record_filename.endswith('.wav'):
        preview_block = """
            {remainder}
            <br>
            <div id="record">
                <audio controls>
                  <source src="{static_url}tmp/dialog/call_records/{filename}" type="audio/wav">
                  Your browser does not support the audio element.
                </audio>
            </div>
        """.format(remainder=preview_block, static_url=STATIC_URL, filename=record_filename)

    return preview_block


def get_map_block(form):
    template = extract_template('map')

    from_coords, to_coords = None, None
    if form['from']:
        from_coords = [form['from']['lat'], form['from']['long']]
    if form['to']:
        to_coords = [form['to']['lat'], form['to']['long']]

    comment = ''
    init_map_code = ''
    if from_coords and to_coords:
        init_map_code = """
            $("#map").parent().parent().attr("class", "panel-collapse collapse show");
            
            map = new ymaps.Map("map", {{
                center: [55.74954, 37.621587],
                zoom: 13
            }});
            
            set_route({from_coords}, {to_coords});
            
            $("#map").parent().parent().attr("class", "panel-collapse collapse out");
        """.format(from_coords=from_coords, to_coords=to_coords)
    else:
        comment = '<p>Заказ не был сформирован</p>'

    return template.format(comment=comment, init_map_code=init_map_code)


def get_webhook_params(token, webhook_id):
    detail_name = 'webhook'

    mock_fail_tts_filename = extract_mock_file('fail_tts_filename', 'other')
    with patch('custom_admin.services.details.requests.get') as mocked_get:
        mocked_get.return_value.json.side_effect = [extract_mock_file('detail', detail_name)] + \
                                                   6 * [mock_fail_tts_filename]
        mocked_get.return_value.status_code = 200

        webhook_params = get_detail_params(token, detail_name, webhook_id)
        if 'error_message' in webhook_params:
            return webhook_params

        webhook_params['can_edit'] = True

        return webhook_params


def get_order_params(token, order_id):
    detail_name = 'order'

    mock_fail_tts_filename = extract_mock_file('fail_tts_filename', 'other')
    with patch('custom_admin.services.details.requests.get') as mocked_get:
        mocked_get.return_value.json.side_effect = [extract_mock_file('detail', detail_name)] + \
                                                   6 * [mock_fail_tts_filename]
        mocked_get.return_value.status_code = 200

        order_params = get_detail_params(token, detail_name, order_id)
        if 'error_message' in order_params:
            return order_params

        order_params['can_edit'] = True

        return order_params
