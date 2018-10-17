from unittest.mock import patch

from django.http import SimpleCookie
from django.test import TestCase
from django.urls import reverse

from custom_admin.services.utils import extract_mock_file, to_normal_time
from custom_admin.tests import *


class IndexTest(TestCase):
    def test_index(self):
        with patch('custom_admin.services.auth.is_authenticated') as is_authenticated:
            is_authenticated.return_value = True

            with patch('custom_admin.services.auth.requests.post') as mocked_post:
                mocked_post.return_value.json = lambda: extract_mock_file('fail_authorize', 'other')
                mocked_post.return_value.status_code = 500

                form_data = {'username': '', 'password': ''}
                resp = self.client.post(reverse('custom_admin:index'), data=form_data)

                self.assertIs(resp.status_code, 200)
                self.assertTemplateUsed(resp, 'custom_admin/error_page.html')

                self.assertDictEqual(resp.context['msg'], {
                    'error_message': 'failed to authorize',
                    'response': extract_mock_file('fail_authorize', 'other'),
                })

            with patch('custom_admin.services.auth.requests.post') as mocked_post:
                mocked_post.return_value.json = lambda: extract_mock_file('authorize', 'other')
                mocked_post.return_value.status_code = 200

                form_data = {'username': '', 'password': ''}
                resp = self.client.post(reverse('custom_admin:index'), data=form_data)

                self.assertIs(resp.status_code, 200)
                self.assertTemplateUsed(resp, 'custom_admin/index.html')

                self.assertEqual(resp.cookies['token'].value, token)


class LogoutTest(TestCase):
    def test_logout(self):
        self.client.cookies = SimpleCookie({'token': token})
        resp = self.client.get(reverse('custom_admin:logout'))

        self.assertIs(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'registration/logged_out.html')

        self.assertNotEqual(resp.cookies['token'], token)


def list_view_test(test_case, resource_name):
    with patch('custom_admin.services.auth.is_authenticated') as is_authenticated:
        is_authenticated.return_value = True

        with patch('custom_admin.services.lists.get_paginator') as paginator:
            paginator.return_value = static_paginator

            mock_fail_get_list = extract_mock_file('fail_list', resource_name[:-1])
            with patch('custom_admin.services.lists.requests.get') as mocked_get:
                mocked_get.return_value.json = lambda: mock_fail_get_list
                mocked_get.return_value.status_code = 500

                test_case.client.cookies = SimpleCookie({'token': token})
                resp = test_case.client.get(reverse('custom_admin:{}'.format(resource_name)))

                test_case.assertIs(resp.status_code, 200)
                test_case.assertTemplateUsed(resp, 'custom_admin/error_page.html')

                test_case.assertDictEqual(resp.context['msg'], {
                    'error_message': 'failed to get {}'.format(resource_name),
                    'response': mock_fail_get_list,
                })

            with patch('custom_admin.services.lists.requests.get') as mocked_get:
                mocked_get.return_value.json = lambda: extract_mock_file('list', resource_name[:-1])
                mocked_get.return_value.status_code = 200

                test_case.client.cookies = SimpleCookie({'token': token})
                resp = test_case.client.get(reverse('custom_admin:{}'.format(resource_name)))

                test_case.assertIs(resp.status_code, 200)
                test_case.assertTemplateUsed(resp, 'custom_admin/list_items.html')

                result = get_result('list', resource_name[:-1])

                for key, val in result.items():
                    if type(val) == list:
                        test_case.assertListEqual(list(resp.context[key]), list(val))
                    else:
                        test_case.assertEqual(resp.context[key], val)


def detail_view_test(test_case, resource_name, detail_id):
    with patch('custom_admin.services.auth.is_authenticated') as is_authenticated:
        is_authenticated.return_value = True

        mock_fail_get_detail = extract_mock_file('fail_detail', resource_name)
        with patch('custom_admin.services.details.requests.get') as mocked_get:
            mocked_get.return_value.json = lambda: mock_fail_get_detail
            mocked_get.return_value.status_code = 500

            test_case.client.cookies = SimpleCookie({'token': token})
            resp = test_case.client.get(reverse('custom_admin:{}'.format(resource_name), args=[detail_id]))

            test_case.assertIs(resp.status_code, 200)
            test_case.assertTemplateUsed(resp, 'custom_admin/error_page.html')

            test_case.assertDictEqual(resp.context['msg'], {
                'error_message': 'failed to get {}'.format(resource_name),
                'response': mock_fail_get_detail,
            })

        mock_fail_tts_filename = extract_mock_file('fail_tts_filename', 'other')
        with patch('custom_admin.services.details.requests.get') as mocked_get:
            mocked_get.return_value.json.side_effect = [extract_mock_file('detail', resource_name)] + \
                                                       6 * [mock_fail_tts_filename]
            mocked_get.return_value.status_code = 200

            test_case.client.cookies = SimpleCookie({'token': token})
            resp = test_case.client.get(reverse('custom_admin:{}'.format(resource_name), args=[detail_id]))

            test_case.assertIs(resp.status_code, 200)
            test_case.assertTemplateUsed(resp, 'custom_admin/detail.html')

            for key, val in get_result('detail', resource_name).items():
                test_case.assertEqual(resp.context[key], val)


def edit_view_test(test_case, resource_name, item_id):
    with patch('custom_admin.services.auth.is_authenticated') as is_authenticated:
        is_authenticated.return_value = True

        mock_fail_change_item = extract_mock_file('fail_change', resource_name)
        with patch('custom_admin.services.modify.requests.put') as mocked_put:
            mocked_put.return_value.json = lambda: mock_fail_change_item
            mocked_put.return_value.status_code = 500

            test_case.client.cookies = SimpleCookie({'token': token})
            resp = test_case.client.post(reverse('custom_admin:edit_{}'.format(resource_name), args=[item_id]), data={})

            test_case.assertIs(resp.status_code, 200)
            test_case.assertTemplateUsed(resp, 'custom_admin/error_page.html')

            test_case.assertDictEqual(resp.context['msg'], {
                'error_message': 'failed to change {}'.format(resource_name),
                'response': mock_fail_change_item,
            })

        mock_change_item = extract_mock_file('change', resource_name)
        with patch('custom_admin.services.modify.requests.put') as mocked_put, \
                patch('custom_admin.services.details.requests.get') as mocked_get:
            mocked_put.return_value.json = lambda: mock_change_item
            mocked_put.return_value.status_code = 200

            mocked_get.return_value.json = lambda: mock_change_item
            mocked_get.return_value.status_code = 200

            test_case.client.cookies = SimpleCookie({'token': token})
            resp = test_case.client.post(reverse('custom_admin:edit_{}'.format(resource_name), args=[item_id]), data={})

            test_case.assertIs(resp.status_code, 200)
            test_case.assertTemplateUsed(resp, 'custom_admin/edit_detail.html')

            detail = get_result('change', resource_name)
            for col_name in ('ctime', 'utime'):
                if col_name in detail:
                    detail[col_name] = to_normal_time(detail[col_name], using_ms=False)

            result = get_result('detail', resource_name)
            result['detail'] = detail
            for key, val in result.items():
                test_case.assertEqual(resp.context[key], val)


class PartnersTest(TestCase):
    def test_partners(self):
        list_view_test(self, 'partners')

    def test_partner(self):
        detail_view_test(self, 'partner', partner_id)

    def test_change_partner(self):
        edit_view_test(self, 'partner', partner_id)


class IntegrationsTest(TestCase):
    def test_integrations(self):
        list_view_test(self, 'integrations')

    def test_integration(self):
        detail_view_test(self, 'integration', integration_id)

    def test_change_integration(self):
        edit_view_test(self, 'integration', integration_id)


class CallsTest(TestCase):
    def test_calls(self):
        list_view_test(self, 'calls')

    def test_call(self):
        detail_view_test(self, 'call', call_id)


# class WebhooksTest(TestCase):
#     def test_webhooks(self):
#         list_view_test(self, 'webhooks')
#
#     def test_webhook(self):
#         detail_view_test(self, 'webhook', webhook_id)
#
#     def test_change_webhook(self):
#         edit_view_test(self, 'webhook', webhook_id)


# class OrdersTest(TestCase):
#     def test_orders(self):
#         list_view_test(self, 'orders')
#
#     def test_order(self):
#         detail_view_test(self, 'order', order_id)
#
#     def test_change_order(self):
#         edit_view_test(self, 'order', order_id)
