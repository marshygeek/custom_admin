import logging
import os
from os.path import join

from custom_admin.apps import CustomAdminConfig

logger = logging.getLogger(CustomAdminConfig.name)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - {} - %(levelname)s - %(message)s'.format(CustomAdminConfig.name.upper()))

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# it's about 2 years
COOKIE_MAX_AGE = 3600 * 24 * 365 * 2

CORE_API_CP1 = 'http://core/cp1/{}'
CORE_API_V1 = 'http://core/v1/{}'
CORE_DEMO_API = 'http://core/demo1/{}'

SYNTAX_API = 'http://syntax:8088/syntax/v1/{}'
GEO_API = 'http://geo:8084/v1/{}'
DIALOG_API = 'http://dialog:8089/v1/{}'

APP_DIR = os.path.dirname(__file__)
MOCK_FILES_DIR = join(APP_DIR, 'mock_files')

SERVICES_TEMPLATES_DIR = join(APP_DIR, join('services', 'templates'))

PAGINATOR_PER_PAGE = 20

SHORT_PARTNER_COLS = ['id', 'login', 'password', 'name', 'organization', 'address']
SHORT_INTEGRATION_COLS = ['id', 'city_id', 'sip', 'phone_number', 'partner_id', 'redirect_to_operator_sip']
SHORT_CALL_COLS = ['id', 'partner_call_id', 'partner_id', 'integration_id', 'customer_id', 'status', 'record', 'ctime', 'utime']
SHORT_WEBHOOK_COLS = ['id', 'url', 'type', 'integration_id', 'method', 'ctime', 'utime']
SHORT_ORDER_COLS = ['id', 'customer_id', 'call_id', 'integration_id', 'city_id', 'partner_id', 'ctime', 'utime']

FULL_PARTNER_COLS = ['id', 'login', 'password', 'name', 'organization', 'address', 'contact_phones', 'description',
                     'emails', 'uuid', 'ctime', 'utime']
FULL_INTEGRATION_COLS = ['id', 'city_id', 'sip', 'phone_number', 'partner_id', 'redirect_to_operator_sip', 'uuid',
                         'ctime', 'utime']
FULL_CALL_COLS = ['id', 'partner_call_id', 'partner_id', 'integration_id', 'customer_id', 'status', 'record',
                  'transcription', 'form', 'uuid', 'ctime', 'utime']
FULL_WEBHOOK_COLS = ['id', 'url', 'type', 'integration_id', 'method', 'uuid', 'ctime', 'utime']
FULL_ORDER_COLS = ['id', 'customer_id', 'call_id', 'integration_id', 'city_id', 'options', 'status',
                   'from_text', 'from_lat', 'from_long', 'to_text', 'to_lat', 'to_long', 'price', 'uuid',
                   'partner_id', 'ctime', 'utime']

COLS_TO_SHORTEN = ['partner_id', 'integration_id', 'customer_id']
