# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from main.models import *
from utils import http, codes, messages

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt


import datetime, time

User = get_user_model()


@csrf_exempt
@http.json_response()
@require_http_methods("POST")
@http.required_parameters(["secret_key"])
@login_required
def kill(request):
	"""
	"""

	username = request.user
	
	secret_key = request.POST["secret_key"]

	player = None
	
	print type(username)

	try:
		player = MainUser.objects.get(username="user1")
	except Exception as e:
		print "shit"


	game_entry_1 = None

	try:
		game_entry_1 = GameEntry.objects.get(player=player)
	except Exception as e:
		pass


	victim = game_entry_1.victim
	game_entry_2 = None
	try:
		game_entry_2 = GameEntry.objects.get(player=victim)
	except Exception as e:
		pass

	log = None

	if game_entry_1.secret_key == secret_key:
		log = KillLog.objects.create_log(entry=game_entry_1)
		entry = game_entry_1
		
		game_entry_1.victim = game_entry_2.victim
		game_entry_1.secret_key = game_entry_2.secret_key
		game_entry_1.kills += 1
		game_entry_2.is_active = False
		game_entry_2.save()
		game_entry_1.save()
	else:
		return http.code_response(codes.WRONG_SECRET_KEY, message=messages.WRONG_SECRET_KEY)

	return {
		"result": game_entry_1.to_json()
	}

