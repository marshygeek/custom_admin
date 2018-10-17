import os
from json import load

from os.path import join

APP_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(APP_DIR, 'results')


def get_result(filename, prefix=''):
    with open(os.path.join(RESULTS_DIR, join(prefix, filename) + '.json'), encoding='utf8') as file:
        return load(file)


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6ImJhOD'

partner_id = 1
integration_id = 2
call_id = 1
webhook_id = 1

static_paginator = {
    'has_previous': False,
    'previous_page_number': 0,
    'number': 1,
    'has_next': True,
    'next_page_number': 2,
    'num_pages': 2
}

tts_filename = '/tmp/dialog/tts/crt/Анна/audio/234-2g32-523g23-gsdg_no_silence.wav'
