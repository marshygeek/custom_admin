from django.test import TestCase
from unittest.mock import patch

from custom_admin.services.auth import authorize
from custom_admin.services.details import *
from custom_admin.services.lists import *
from custom_admin.services.modify import *
from custom_admin.services.utils import extract_mock_file
from custom_admin.services.tts_generation import get_tts_filename
from custom_admin.tests import *


class AuthTest(TestCase):
    def test_authorize(self):
        with patch('custom_admin.services.auth.requests.post') as mocked_post:
            mocked_post.return_value.json = lambda: extract_mock_file('fail_authorize', 'other')
            mocked_post.return_value.status_code = 500

            result = authorize("", "")
            self.assertDictEqual(result, {
                'error_message': 'failed to authorize',
                'response': extract_mock_file('fail_authorize', 'other'),
            })

        with patch('custom_admin.services.auth.requests.post') as mocked_post:
            mocked_post.return_value.json = lambda: extract_mock_file('authorize', 'other')
            mocked_post.return_value.status_code = 200

            result_token = authorize("", "")
            self.assertEqual(result_token, token)


class ListsTest(TestCase):
    def get_list_params_test(self, resource_name, get_list_params_method):
        with patch('custom_admin.services.lists.get_paginator') as paginator:
            paginator.return_value = static_paginator

            mock_fail_get_list = extract_mock_file('fail_list', resource_name[:-1])
            with patch('custom_admin.services.lists.requests.get') as mocked_get:
                mocked_get.return_value.json = lambda: mock_fail_get_list
                mocked_get.return_value.status_code = 500

                list_params = get_list_params_method("", {})
                self.assertDictEqual(list_params, {
                    'error_message': 'failed to get {}'.format(resource_name),
                    'response': mock_fail_get_list,
                })

            with patch('custom_admin.services.lists.requests.get') as mocked_get:
                mocked_get.return_value.json = lambda: extract_mock_file('list', resource_name[:-1])
                mocked_get.return_value.status_code = 200

                list_params = get_list_params_method("", {})
                self.assertDictEqual(list_params, get_result('list', resource_name[:-1]))

    def test_get_partners_params(self):
        self.get_list_params_test('partners', get_partners_params)

    def test_get_integrations_params(self):
        self.get_list_params_test('integrations', get_integrations_params)

    def test_get_calls_params(self):
        resource_name = 'calls'
        self.get_list_params_test(resource_name, get_calls_params)

        # testing case with breadcrumbs
        with patch('custom_admin.services.lists.get_paginator') as paginator:
            paginator.return_value = static_paginator
            with patch('custom_admin.services.lists.requests.get') as mocked_get:
                mocked_get.return_value.json = lambda: extract_mock_file('list', resource_name[:-1])
                mocked_get.return_value.status_code = 200

                list_params = get_calls_params("", {'transit': 1})
                self.assertDictEqual(list_params, get_result('list2', resource_name[:-1]))

    # def test_get_webhooks_params(self):
    #     self.get_list_params_test('webhooks', get_webhooks_params)

    # def test_get_orders_params(self):
    #     self.get_list_params_test('orders', get_orders_params)


class DetailsTest(TestCase):
    def get_detail_params_test(self, resource_name, get_detail_params_method, detail_id):
        mock_fail_get_detail = extract_mock_file('fail_detail', resource_name)
        with patch('custom_admin.services.details.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: mock_fail_get_detail
            mocked_get.return_value.status_code = 500

            detail_params = get_detail_params_method("", detail_id)
            self.assertDictEqual(detail_params, {
                'error_message': 'failed to get {}'.format(resource_name),
                'response': mock_fail_get_detail,
            })

        mock_fail_tts_filename = extract_mock_file('fail_tts_filename', 'other')
        with patch('custom_admin.services.details.requests.get') as mocked_get:
            mocked_get.return_value.json.side_effect = [extract_mock_file('detail', resource_name)] + \
                                                       6 * [mock_fail_tts_filename]
            mocked_get.return_value.status_code = 200

            detail_params = get_detail_params_method("", detail_id)
            self.assertDictEqual(detail_params, get_result('detail', resource_name))

    def test_get_partner_params(self):
        self.get_detail_params_test('partner', get_partner_params, partner_id)

    def test_get_integration_params(self):
        self.get_detail_params_test('integration', get_integration_params, integration_id)

    def test_get_call_params(self):
        self.get_detail_params_test('call', get_call_params, call_id)

    # def test_get_webhook_params(self):
    #     self.get_detail_params_test('webhook', get_webhook_params, webhook_id)

    # def test_get_order_params(self):
    #     self.get_detail_params_test('order', get_order_params, order_id)


class ModifyTest(TestCase):
    def change_item_test(self, resource_name, change_item_method, item_id, item_params):
        mock_fail_change_item = extract_mock_file('fail_change', resource_name)
        with patch('custom_admin.services.modify.requests.put') as mocked_put:
            mocked_put.return_value.json = lambda: mock_fail_change_item
            mocked_put.return_value.status_code = 500

            result = change_item_method("", item_id, item_params)
            self.assertDictEqual(result, {
                'error_message': 'failed to change {}'.format(resource_name),
                'response': mock_fail_change_item,
            })

        with patch('custom_admin.services.modify.requests.put') as mocked_put:
            mocked_put.return_value.json = lambda: extract_mock_file('change', resource_name)
            mocked_put.return_value.status_code = 200

            result = change_item_method("", item_id, item_params)
            self.assertDictEqual(result, get_result('change', resource_name))

    def test_get_partner_params(self):
        self.change_item_test('partner', change_partner, partner_id, {})

    def test_get_integration_params(self):
        self.change_item_test('integration', change_integration, integration_id, {})

    # def test_get_webhook_params(self):
    #     self.change_item_test('webhook', change_webhook, webhook_id, {})

    # def test_get_order_params(self):
    #     self.change_item_test('order', change_order, order_id, {})


class UtilsTest(TestCase):
    def test_get_tts_filename(self):
        mock_fail_tts_filename = extract_mock_file('fail_tts_filename', 'other')
        with patch('custom_admin.services.tts_generation.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: mock_fail_tts_filename
            mocked_get.return_value.status_code = 404

            result = get_tts_filename('')
            self.assertDictEqual(result, {
                'error_message': 'failed to get tts filename',
                'response': mock_fail_tts_filename,
            })

        with patch('custom_admin.services.tts_generation.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: extract_mock_file('tts_filename', 'other')
            mocked_get.return_value.status_code = 200

            result = get_tts_filename('')
            self.assertEqual(result, tts_filename)
