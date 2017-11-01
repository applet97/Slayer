# -*- coding: utf-8 -*-

from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
# from main.messages import *
from main.models import GameEntry, KillLog, Game

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta
import datetime, time

from avatar.models import Avatar
from utils import string_del
from utils.messages import *

User = get_user_model()


@login_required
def basic(request):
    template = 'main/main.html'
    params = dict()
    params['me'] = request.user
    my_entry = None

    try:
        my_entry = GameEntry.objects.get(player=request.user)
    except Exception as e:
        
        pass
    


    if my_entry is not None: 

        victime_entry = None
        try:
            victim_entry = GameEntry.objects.get(player=my_entry.victim)
        except Exception as e:

            pass


        params['my_entry'] = my_entry
        params['secret_key'] = my_entry.secret_key
        params['victim'] = my_entry.victim
        
        params['victim_entry'] = victim_entry
        params['game'] = my_entry.game
        delta = Game.objects.first().start_date - datetime.datetime.now()
        params['game_start_left'] = delta.days * 24 * 60 * 60 +  delta.seconds

        parent_entry = None
        try:
            parent_entry = GameEntry.objects.get(victim=my_entry.player)
        except Exception as e:
            pass

        params['parent_entry'] = parent_entry

        if my_entry.player == my_entry.victim:
            params['winner'] = my_entry.player

        elif request.method == "POST":

            victim_entry = get_object_or_404(GameEntry, player=my_entry.victim)

            secret_key = request.POST.get('secret_key')

            if secret_key != "":
                
                if my_entry.status is GameEntry.KILLED:
                    messages.add_message(request, messages.WARNING, YOU_WERE_KILLED)
                elif secret_key == victim_entry.secret_key:
                    messages.add_message(request, messages.SUCCESS, SUCCESS_KILL)
                    KillLog.objects.create_log(entry=my_entry)
                    victim_entry.status = GameEntry.KILLED
                    victim_entry.save()
                    my_entry.victim = victim_entry.victim
                    my_entry.kills += 1
                    my_entry.save()

                    params['my_entry'] = my_entry
                    params['victim'] = my_entry.victim
                    victim_entry = get_object_or_404(GameEntry, player=my_entry.victim)
                    params['victim_entry'] = victim_entry

                    if my_entry.player == my_entry.victim:
                        params['winner'] = my_entry.player
                else:
                    messages.add_message(request, messages.WARNING, NOT_GOOD_SECRET_KEY)
    else:
        print "blyaat"

    return render(request, template, params)


@login_required
def rating(request):
    template = 'main/rating.html'
    params = dict()
    params['me'] = request.user
    results = list()

    params['total_count'] = GameEntry.objects.filter(player__is_superuser=False).count()
    params['alive_count'] = GameEntry.objects.filter(player__is_superuser=False, status=GameEntry.ALIVE).count()

    # entries = GameEntry.objects.filter(player__is_superuser=False).order_by('status', '-kills')
    params['entries'] = GameEntry.objects.filter(player__is_superuser=False).order_by('status', '-kills', 'player')
    

    return render(request, template, params)


@login_required
def history(request):
    template = 'main/history.html'
    params = dict()
    params['me'] = request.user
    
    results = list()
    params['killer_logs'] = request.user.killer_logs.all()
    print params['killer_logs']

    return render(request, template, params)