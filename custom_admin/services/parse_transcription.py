from al_admin.settings import STATIC_URL
from custom_admin.services.tts_generation import get_tts_filename
from custom_admin.services.utils import extract_template, to_normal_time, pretty_dumps


def generate_detail_block(detail_transcription):
    detail_block = '<h2>Диалог:</h2>\n'
    for element in detail_transcription:
        if element['type'] == 'output':
            rendered_el = generate_output(element)
        elif element['type'] == 'input':
            rendered_el = generate_input(element)
        elif element['type'] == 'hangup':
            rendered_el = generate_hangup(element)
        else:
            rendered_el = generate_timeout(element)

        detail_block += '<div>{}</div><hr>\n'.format(rendered_el)

    return detail_block


def generate_output(out_msg):
    template = extract_template('output', 'transcription')

    phrase = out_msg['phrase']
    result = get_tts_filename(phrase, from_cache=True)
    if 'error_message' in result:
        tts_filename = '/-'
    else:
        tts_filename = result

    return template.format(
        phrase=phrase,
        time=to_normal_time(out_msg['time']),
        body=pretty_dumps(out_msg),
        tts_filename=f'{STATIC_URL}{tts_filename[1:]}',
    )


def generate_input(in_msg):
    template = extract_template('input', 'transcription')

    phrases = ' | '.join([variant['text'] for variant in in_msg['message']['result']])

    return template.format(
        phrases=phrases,
        time=to_normal_time(in_msg['time']),
        body=pretty_dumps(in_msg)
    )


def generate_timeout(timeout):
    template = extract_template('timeout', 'transcription')

    return template.format(
        time=to_normal_time(timeout['time']),
        body=pretty_dumps(timeout)
    )


def generate_hangup(hangup):
    template = extract_template('hangup', 'transcription')

    if hangup['client']:
        direction = 'client'
    else:
        direction = 'dialog'
    return template.format(
        time=to_normal_time(hangup['time']),
        direction=direction,
        body=pretty_dumps(hangup)
    )
