import functools

from api import codes

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

from api.utils import token, string_utils
from functools import wraps

import datetime


import json

import string_utils


def check_secret():
    """
    checks application secret
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            value = request.META.get('HTTP_SUPER_SECRET_APP_SECRET')
            if value != settings.SECRET_KEY:
                return code_response(codes.MISSING_SECRET_KEY)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def required_session_params(params_list):
    """
    Decorator to make a view only accept request.session with required parameters.
    :param params_list: list of required parameters.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            for parameter in params_list:
                value = request.session.get(parameter)
                if value is None:
                    return code_response(codes.MISSING_SESSION_PARAMS)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def required_request_params(params_list):
    """
    Decorator to make a view only accept request with required parameters.
    :param params_list: list of required parameters.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method == "POST":
                for parameter in params_list:
                    value = string_utils.empty_to_none(request.POST.get(parameter))
                    if value is None:
                        return code_response(codes.MISSING_REQUEST_PARAMS)
            else:
                for parameter in params_list:
                    value = string_utils.empty_to_none(request.GET.get(parameter))
                    if value is None:
                        return code_response(codes.MISSING_REQUEST_PARAMS)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def http_response_with_json(python_dict):
    return HttpResponse(json.dumps(python_dict), content_type="application/json")


def json_response():
    """
    Decorator that wraps response into json.
    """
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            if not ('code' in response):
                response['code'] = codes.OK
            return http_response_with_json(response)
        return inner
    return decorator


def code_response(code, message=None):
    result = {
        'code': code
    }
    if message:
        result['message'] = message
    return result



def ok_response():
    return code_response(codes.OK)


def extract_token_from_request(request):
    """
    Extracts token string from request. First tries to get it from AUTH_TOKEN header,
    if not found (or empty) tries to get from cookie.
    :param request:
    :return: Token string found in header or cookie; null otherwise.
    """
    header_names_list = settings.AUTH_TOKEN_HEADER_NAME

    token_string = None
    for name in header_names_list:
        if name in request.META:
            token_string = string_utils.empty_to_none(request.META[name])

    if token_string is None:
        token_string = request.COOKIES.get(settings.AUTH_TOKEN_COOKIE_NAME, None)

    if token_string is None:
        token_string = request.POST.get(settings.AUTH_TOKEN_COOKIE_NAME, None)            
    return string_utils.empty_to_none(token_string)


def requires_token():
    """
    Decorator to make a view only accept request with valid token.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            token_string = extract_token_from_request(request)
            if token_string is None:
                if request.user.is_authenticated():
                    return func(request, *args, **kwargs)
                return code_response(codes.BAD_REQUEST)
            result = token.verify_token(token_string)
            if result is None:
                return code_response(codes.TOKEN_INVALID)
            request.session['username'] = result['username']
            return func(request, *args, **kwargs)
        return inner
    return decorator
