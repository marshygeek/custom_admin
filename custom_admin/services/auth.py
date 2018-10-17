import requests
from django.shortcuts import redirect
from django.urls import reverse

from custom_admin.config import CORE_API_CP1
from custom_admin.services.common import render_error_page
from custom_admin.services.utils import wrap_request_method, handle_request_errors


def authentication_required(view):
    def wrapper(request, *args, **kwargs):
        if 'token' not in request.COOKIES:
            return redirect(reverse('login'))

        result = is_authenticated(request.COOKIES['token'])
        if type(result) != bool:
            # error occurred
            return render_error_page(request, result)
        elif not result:
            return redirect(reverse('login'))
        else:
            return view(request, *args, **kwargs)

    return wrapper


def authorize(username, password):
    url = CORE_API_CP1.format('oauth/authorize')
    request_method = wrap_request_method(requests.post, url, json={
        'username': username,
        'password': password,
        'grant_type': 'password',
        'client_id': 'AlPlatform'
    })

    content = handle_request_errors(request_method, 'authorize')
    if 'error_message' in content:
        return content

    # return token
    return content['access_token']


def is_authenticated(token):
    # core doesn't have method to check validity of a token, using 'partners' endpoint instead
    url = CORE_API_CP1.format('partners')

    payload = {
        'access_token': token,
    }
    request_method = wrap_request_method(requests.get, url, params=payload)

    content = handle_request_errors(request_method, 'get partners (unauthenticated)')

    if 'error_message' not in content:
        return True
    elif 'error' in content['response'] and content['response']['error'] == 'invalid_token':
        return False
    else:
        return content
