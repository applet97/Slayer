# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api.utils import token, utils
from api.utils import decorators as decors
from api import codes, messages
from django.db.models import Q

from main.models import TokenLog#, EmailConfirmation
from main import tasks
import hashlib
from django.template.loader import render_to_string

User = get_user_model()


@csrf_exempt
@decors.json_response()
@require_http_methods("POST")
@decors.required_request_params(["username", "password"])
def login(request):
    """
    Simple authentification
    if OK, returns token
    """
    username = request.POST["username"]
    password = request.POST["password"]
    # authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return {
            'code': codes.WRONG_PASSWORD,
            'message': messages.WRONG_PASSWORD
        }
    if not user.is_active:
        return decors.code_response(codes.USER_NOT_ACTIVE)
    created_token = token.create_token(user=user)
    return {
            "token": created_token,
            "user": user.to_json()
    }


@csrf_exempt
@decors.json_response()
@decors.requires_token()
@require_http_methods("POST")
def logout(request):
    """
    Deletes token from database
    """
    token_string = decors.extract_token_from_request(request)
    try:
        TokenLog.objects.filter(token=token_string).update(deleted=True)
        return decors.ok_response()         
    except Exception as e:
        return {
            'code': codes.SERVER_ERROR,
            'message': str(e)
        }


@csrf_exempt
@decors.json_response()
@decors.required_request_params(['username', 'password', 'email'])
@require_http_methods("POST")
def register(request):
    """
    Simple registration
    if OK, returns token
    """
    username = request.POST['username']
    email = request.POST.get('email')
    password = request.POST['password']
    # TODO email regex check
    if email is not None or email != '':
        if User.objects.filter(email=email, email_approved=True).exists():
            return decors.code_response(code=codes.EMAIL_ALREADY_EXISTS, message=messages.EMAIL_ALREADY_EXISTS)
    if User.objects.filter(username=username).exists():
        return decors.code_response(code=codes.INVALID_FORM, message=messages.USER_ALREADY_EXISTS)
    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    created_token = token.create_token(user=user)
    #EmailConfirmation.objects.create_confirmation(user)
    return {
        'user': user.to_json(),
        'token': created_token
    }


@csrf_exempt
@decors.json_response()
@require_http_methods("POST")
@decors.required_request_params(['username'])
def forgot_password(request):
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        return decors.code_response(codes.BAD_REQUEST, message=messages.USER_NOT_FOUND)
    if not user.email_approved:
        return decors.code_response(codes.BAD_REQUEST, message=messages.EMAIL_NOT_APPROVED)
    new_password = utils.generate_random_pass(10)
    user.set_password(new_password)
    user.save()
    tasks.email.delay(to=user.email, subject=messages.NEW_PASSWORD, \
        message=render_to_string('emails/new_password.txt', {'new_password': new_password}))
    return decors.code_response(code=codes.OK, message=messages.PASSWORD_SENT_TO_EMAIL)

