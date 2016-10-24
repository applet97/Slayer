# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from main.models import GameEntry, Game
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


def generate(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Command(BaseCommand):

    help = 'Creates entries'

    def handle(self, *args, **options):
        game = Game.objects.first()
        users = User.objects.filter(is_superuser=False)
        for user in users:
            entry, _ = GameEntry.objects.get_or_create(game=game, player=user)
            entry.status = GameEntry.ALIVE
            entry.secret_key = generate()
            entry.save()
            print entry.player.username + "`s entry was successfully created"
