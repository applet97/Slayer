# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from api.utils import decorators as decors, constants, utils, string_utils
from api import codes, messages, constants
from django.db.models import Q

from main.models import Game, GameEntry, KillLog

import os
import json

User = get_user_model()


@csrf_exempt
@decors.json_response()
@decors.requires_token()
@decors.required_session_params(['username'])
@require_http_methods("POST")
@decors.required_request_params(['game_id'])
def register(request):
    """
    View for registering to game
    """
    try:
    	user = User.objects.get(username=request.SESSION['username'])
        game = Game.objects.get(pk=request.POST['game_id'])
    except:
    	return decors.code_response(code=codes.BAD_REQUEST, message=messages.GAME_OR_USER_NOT_FOUND)
    if game.status != Game.NOT_STARTED:
    	return decors.code_response(code=codes.BAD_REQUEST, message=messages.GAME_STARTED)
    if GameEntry.objects.filter(game=game, player=user).exists():
    	return decors.code_response(code=codes.BAD_REQUEST, message=messages.USER_ALREADY_REGISTERED)
    game_entry = GameEntry.objects.create(game=game, player=user)
    return {
        'result': game_entry.to_json(),
        'message': messages.SUCCESS_REGISTRATION
    }


@csrf_exempt
@decors.json_response()
@decors.requires_token()
@decors.required_session_params(['username'])
@require_http_methods("POST")
@decors.required_request_params(['game_id'])
def games(request):
    """
    View for getting list of games
    """
    statuses = request.POST.getlist('statuses[]')
    if len(statuses) == 0:
        statuses = constants.GAME_STATUSES_LIST
    else:
        statuses = string_utils.integer_list(statuses)
    return {
        'result': Game.objects.filter(status__in=statuses)
    }


@csrf_exempt
@decors.json_response()
@decors.requires_token()
@decors.required_session_params(['username'])
@require_http_methods("POST")
@decors.required_request_params(['game_id', 'secret_key'])
def kill(request):
	"""
	View for killing the victim
	"""
    try:
    	try:
    	    game = Game.objects.get(pk=request.POST['game_id'])
    	except:
    		return decors.code_response(code=codes.BAD_REQUEST, message=messages.GAME_OR_USER_NOT_FOUND)
    	game_entry = game.game_entries.filter(player__username=request.SESSION['username']).first()
        victim_entry = game.game_entries.filter(player=game_entry.victim).first()
        if victim_entry.secret_key != request.POST['secret_key']
            return decors.code_response(code=codes.BAD_REQUEST, message=messages.SECRET_KEY_NOT_VALID)
        KillLog.objects.create_log(game=game, killer=game_entry.player, victim=game_entry.victim)
        game_entry.kills += 1
        game_entry.victim = victim_entry.victim
        game_entry.save()
        victim_entry.status = GameEntry.KILLED
        victim_entry.save()
        return {
            'game_entry': game_entry.to_json(),
            'message': messages.SUCCESS_KILL
        }
    except Exception as e:
    	print str(e)


@csrf_exempt
@decors.json_response()
@decors.requires_token()
@decors.required_session_params(['username'])
@require_http_methods("POST")
@decors.required_request_params(['game_id', 'is_my'])
def kill_logs(request):
	"""
	View for retrieving list of kill logs
	"""
    result = dict()
    logs = list()
    if request.POST['is_my'] == "yes":
        logs = [x.to_json() for x in KillLog.objects.filter(game__id=request.POST['game_id'], \
            killer__username=request.SESSION['username'])]
    else:
        logs = [x.to_json() for x in KillLog.objects.filter(game__id=request.POST['game_id'])]
    result['killer_logs'] = logs
    return result

