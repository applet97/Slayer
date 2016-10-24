# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from main.models import GameEntry, Game
from django.contrib.auth import get_user_model
from django.db import transaction
import random

User = get_user_model()


class Command(BaseCommand):

    help = 'Shuffles entries'

    @transaction.atomic
    def handle(self, *args, **options):
        game = Game.objects.first()
        if game.shuffled:
            print "Game is shuffled"
        else:
            entries = list(game.game_entries.filter(player__is_superuser=False, player__is_active=True))
            random.shuffle(entries)
            try:
                for i in xrange(len(entries)-1):
                    entries[i].victim = entries[i+1].player
                    entries[i].save()
                entries[len(entries)-1].victim = entries[0].player
                entries[len(entries)-1].save()
                game.shuffled = True
                game.save()
                print "Success"
            except Exception as e:
                print "Error %s" % str(e)
