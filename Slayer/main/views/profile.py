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
def profile(request):

	return render(request, 'main/profile.html')


@login_required
def change_password(request):
	"""
	View for changing password
	"""
	if request.method == "POST":
		try:
			old_pass = request.POST['old_password']
			new_pass = request.POST['new_password']
			new_pass1 = request.POST['new_password1']
			if not request.user.check_password(old_pass):
				messages.add_message(request, messages.WARNING, ERROR_OLD_PASS)
				return render(request, 'main/change_password.html')
			if new_pass != new_pass1:
				messages.add_message(request, messages.WARNING, PASSWORDS_DONT_MATCH)
				return render(request, 'main/change_password.html')
			request.user.set_password(new_pass)
			request.user.save()
			messages.add_message(request, messages.SUCCESS, SUCCESS)
		except:
			messages.add_message(request, messages.WARNING, ERROR)
	return render(request, 'main/change_password.html')
	
