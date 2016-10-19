# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings
from api.utils import decorators
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

import datetime, time

from main.models import Question
from moderators.models import ModeratorLog
from moderators import messages as msgs

from moderators.forms import QuestionCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

User = get_user_model()


@login_required
def shuffle(request, _id):
    try:
        game = Game.objects.get(_id)
        if game.shuffled == True:
            pass # return with error
        game_entries = game.game_entries.all()
        entries_to_pop = game_entries.copy()
        for entry in game_entries:
            _rand = -1
            while(True):
                _rand = random.randint(0, len(entries_to_pop)-1)
                _entry = entries_to_pop[_rand]
                if entry != _entry:
                    break
            entry.victim = _entry.player
            entry.save()
            entries_to_pop.pop(_rand)
    except Exception as e:
        print str(e)

