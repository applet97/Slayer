# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import *

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from utils.messages import INVALID_USER

import datetime, time

User = get_user_model()


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('main:login'))


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.WARNING, INVALID_USER)
            return redirect(reverse('main:login'))
        auth_login(request, user)
        return redirect(reverse('main:main_page'))

    return render(request, 'main/login.html')