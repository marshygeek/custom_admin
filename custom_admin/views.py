from django.shortcuts import render

from custom_admin.forms import TestGeoSyntaxForm, TTSGenForm
from custom_admin.services.auth import *
from custom_admin.services.common import render_error_page
from custom_admin.services.demo_calls.common import get_cities_list
from custom_admin.services.details import *
from custom_admin.services.lists import *
from custom_admin.services.modify import *
from custom_admin.services.test_geo_syntax import *
from custom_admin.services.tts_generation import *


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    response = render(request, 'registration/logged_out.html')
    response.delete_cookie('token')
    return response


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        result = authorize(username, password)
        if 'error_message' in result:
            return render_error_page(request, result)

        response = render(request, 'custom_admin/index.html')
        response.set_cookie('token', result, max_age=COOKIE_MAX_AGE)

        return response
    else:
        def _view(_request):
            return render(_request, 'custom_admin/index.html')

        return authentication_required(_view)(request)


# PARTNERS
@authentication_required
def partners(request):
    partners_params = get_partners_params(request.COOKIES['token'], request.GET)
    if 'error_message' in partners_params:
        return render_error_page(request, partners_params)

    return render(request, 'custom_admin/list_items.html', partners_params)


@authentication_required
def partner(request, partner_id):
    partner_params = get_partner_params(request.COOKIES['token'], partner_id)
    if 'error_message' in partner_params:
        return render_error_page(request, partner_params)

    return render(request, 'custom_admin/detail.html', partner_params)


@authentication_required
def edit_partner(request, partner_id):
    token = request.COOKIES['token']

    if request.method == 'POST':
        result = change_partner(token, partner_id, request.POST)
        if 'error_message' in result:
            return render_error_page(request, result)

    partner_params = get_partner_params(token, partner_id)
    if 'error_message' in partner_params:
        return render_error_page(request, partner_params)

    return render(request, 'custom_admin/edit_detail.html', partner_params)


@authentication_required
def delete_partner(request, partner_id):
    # perform deletion

    if request.GET.get('to-list'):
        return redirect(reverse('custom_admin:partners'))
    else:
        return render(request, 'custom_admin/delete_success.html', {'list_endpoint': reverse('custom_admin:partners')})


# INTEGRATIONS
@authentication_required
def integrations(request):
    integrations_params = get_integrations_params(request.COOKIES['token'], request.GET)
    if 'error_message' in integrations_params:
        return render_error_page(request, integrations_params)

    return render(request, 'custom_admin/list_items.html', integrations_params)


@authentication_required
def integration(request, integration_id):
    integration_params = get_integration_params(request.COOKIES['token'], integration_id)
    if 'error_message' in integration_params:
        return render_error_page(request, integration_params)

    return render(request, 'custom_admin/detail.html', integration_params)


@authentication_required
def edit_integration(request, integration_id):
    token = request.COOKIES['token']

    if request.method == 'POST':
        result = change_integration(token, integration_id, request.POST)
        if 'error_message' in result:
            return render_error_page(request, result)

    integration_params = get_integration_params(request.COOKIES['token'], integration_id)
    if 'error_message' in integration_params:
        return render_error_page(request, integration_params)

    return render(request, 'custom_admin/edit_detail.html', integration_params)


@authentication_required
def delete_integration(request, integration_id):
    # perform deletion

    if request.GET.get('to-list'):
        return redirect(reverse('custom_admin:integrations'))
    else:
        return render(request, 'custom_admin/delete_success.html',
                      {'list_endpoint': reverse('custom_admin:integrations')})


# CALLS
@authentication_required
def calls(request):
    calls_params = get_calls_params(request.COOKIES['token'], request.GET)
    if 'error_message' in calls_params:
        return render_error_page(request, calls_params)

    return render(request, 'custom_admin/list_items.html', calls_params)


@authentication_required
def call(request, call_id):
    call_params = get_call_params(request.COOKIES['token'], call_id)
    if 'error_message' in call_params:
        return render_error_page(request, call_params)

    return render(request, 'custom_admin/detail.html', call_params)


@authentication_required
def delete_call(request, call_id):
    # perform deletion

    if request.GET.get('to-list'):
        return redirect(reverse('custom_admin:calls'))
    else:
        return render(request, 'custom_admin/delete_success.html', {'list_endpoint': reverse('custom_admin:calls')})


# WEBHOOKS
@authentication_required
def webhooks(request):
    webhooks_params = get_webhooks_params(request.COOKIES['token'], request.GET)
    if 'error_message' in webhooks_params:
        return render_error_page(request, webhooks_params)

    return render(request, 'custom_admin/list_items.html', webhooks_params)


@authentication_required
def webhook(request, webhook_id):
    webhook_params = get_webhook_params(request.COOKIES['token'], webhook_id)
    if 'error_message' in webhook_params:
        return render_error_page(request, webhook_params)

    return render(request, 'custom_admin/detail.html', webhook_params)


@authentication_required
def edit_webhook(request, webhook_id):
    token = request.COOKIES['token']

    if request.method == 'POST':
        result = change_webhook(token, webhook_id, request.POST)
        if 'error_message' in result:
            return render_error_page(request, result)

    webhook_params = get_webhook_params(token, webhook_id)
    if 'error_message' in webhook_params:
        return render_error_page(request, webhook_params)

    return render(request, 'custom_admin/edit_detail.html', webhook_params)


@authentication_required
def delete_webhook(request, webhook_id):
    # perform deletion

    if request.GET.get('to-list'):
        return redirect(reverse('custom_admin:webhooks'))
    else:
        return render(request, 'custom_admin/delete_success.html', {'list_endpoint': reverse('custom_admin:webhooks')})


# ORDERS
@authentication_required
def orders(request):
    orders_params = get_orders_params(request.COOKIES['token'], request.GET)
    if 'error_message' in orders_params:
        return render_error_page(request, orders_params)

    return render(request, 'custom_admin/list_items.html', orders_params)


@authentication_required
def order(request, order_id):
    order_params = get_order_params(request.COOKIES['token'], order_id)
    if 'error_message' in order_params:
        return render_error_page(request, order_params)

    return render(request, 'custom_admin/detail.html', order_params)


@authentication_required
def edit_order(request, order_id):
    token = request.COOKIES['token']

    if request.method == 'POST':
        result = change_order(token, order_id, request.POST)
        if 'error_message' in result:
            return render_error_page(request, result)

    order_params = get_order_params(token, order_id)
    if 'error_message' in order_params:
        return render_error_page(request, order_params)

    return render(request, 'custom_admin/edit_detail.html', order_params)


@authentication_required
def delete_order(request, order_id):
    # perform deletion

    if request.GET.get('to-list'):
        return redirect(reverse('custom_admin:orders'))
    else:
        return render(request, 'custom_admin/delete_success.html', {'list_endpoint': reverse('custom_admin:orders')})


@authentication_required
def test_geo_syntax(request):
    result = get_cities_list()
    if 'error_message' in result:
        return render_error_page(request, result)

    if request.method == 'POST':
        form = TestGeoSyntaxForm(request.POST)
        form.set_cities_choices(result)

        if form.is_valid():
            query_text = form.cleaned_data['query_text']
            city_id = form.cleaned_data["city_id"]

            params = get_test_service_params(city_id, query_text)
            params['form'] = form
            response = render(request, 'custom_admin/test_geo_syntax.html', params)

            return response
    else:
        form = TestGeoSyntaxForm()
        form.set_cities_choices(result)

    # return the form to let user correct the fields
    return render(request, 'custom_admin/test_geo_syntax.html', {'form': form})


@authentication_required
def tts_generation(request):
    if request.method == 'POST':
        form = TTSGenForm(request.POST)

        if form.is_valid():
            query_text = form.cleaned_data['query_text']

            params = get_tts_generation_params(query_text)
            params['form'] = form
            response = render(request, 'custom_admin/tts_generation.html', params)

            return response
    else:
        form = TTSGenForm()

    # return the form to let user correct the fields
    return render(request, 'custom_admin/tts_generation.html', {'form': form})
