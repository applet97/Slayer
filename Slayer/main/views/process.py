# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from main.messages import *

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required

import datetime, time


@login_required
def basic(request):
	template = 'main/main.html'
	params = dict()
	results = list()
	return render(request, template, params)