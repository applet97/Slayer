# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from main.messages import *
from main.models import GameEntry, KillLog

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required

import datetime, time

User = get_user_model()


@login_required
def basic(request):
    template = 'main/main.html'
    params = dict()
    params['me'] = request.user
    my_entry = get_object_or_404(GameEntry, player=request.user)
    params['secret_key'] = my_entry.secret_key
    params['victim'] = my_entry.victim
    params['my_entry'] = my_entry
    if request.method == "POST":
        # kill process
        victim_entry = get_object_or_404(GameEntry, player=my_entry.victim)
        secret_key = request.POST.get('secret_key')
        if secret_key == victim_entry.secret_key:
            messages.add_message(request, messages.SUCCESS, SUCCESS_KILL)
            KillLog.objects.create_log(entry=my_entry)
            victim_entry.status = GameEntry.KILLED
            victim_entry.save()
            my_entry.victim = victim_entry.victim
            my_entry.save()
            KillLog.objects.create_log(entry=my_entry)
        else:
            messages.add_message(request, messages.WARNING, NOT_GOOD_SECRET_KEY)
    return render(request, template, params)


@login_required
def rating(request):
    template = 'main/rating.html'
    params = dict()
    params['me'] = request.user
    results = list()
    params['entries'] = GameEntry.objects.filter(player__is_superuser=False).order_by('kills')
    print params
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
