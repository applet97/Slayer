# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models import Count
from random import randint
import datetime
import time
import random
import hashlib
from django.template.loader import render_to_string

from avatar.models import Avatar


class MainUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a user with the given iin and password
        """
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given iin and password
        """
        user = self.create_user(username, password=password)
        user.is_superuser = True
        user.is_moderator = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    """
    Model for storing main user
    """
    username = models.CharField(max_length=9, blank=False, null=False, db_index=True, unique=True, verbose_name=u'Логин',)
    email = models.EmailField(max_length=100, blank=True, verbose_name=u'email')
    email_approved = models.BooleanField(default=False, blank=True, verbose_name=u'Имейл подтвержден')

    first_name = models.CharField(max_length=255, blank=True, verbose_name=u'Имя')
    middle_name = models.CharField(max_length=255, blank=True, verbose_name=u'Отчество')
    second_name = models.CharField(max_length=255, blank=True, verbose_name=u'Фамилия')
    school = models.CharField(max_length=100, blank=True, verbose_name=u'Школа')

    is_active = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MainUserManager()

    NOT_SELECTED = 0
    MALE = 1
    FEMALE = 2

    GENDERS = (
        (NOT_SELECTED, u'Не выбрано'),
        (MALE, u'Мужчина'),
        (FEMALE, u'Женщина')
        )
    gender = models.SmallIntegerField(blank=True, choices=GENDERS, default=0, verbose_name=u'Пол')
    approved = models.BooleanField(default=False)

    NOT_SELECTED = 0
    ALMATY = 1
    ASTANA = 2
    KARAGANDA = 3
    SHYMSIDE = 4
    TARAZ = 5
    AKTOBE = 6
    KOSTANAY = 7
    AKTAU = 8
    ATYRAU = 9
    URALSK = 10
    PAVLODAR = 11
    USKAMAN = 12
    KOKSHETAU = 13
    TALDIK = 14
    PETROPAVL = 15
    SEMEY = 16
    KYZYLORDA = 17
    ZHEZKAZGAN = 18

    CITIES = (
        (NOT_SELECTED, u'Не выбрано'),
        (ALMATY, u'Алматы'),
        (ASTANA, u'Астана'),
        (KARAGANDA, u'Караганда'),
        (SHYMSIDE, u'Шымкент'),
        (TARAZ, u'Тараз'),
        (AKTOBE, u'Актобе'),
        (KOSTANAY, u'Костанай'),
        (AKTAU, u'Актау'),
        (ATYRAU, u'Атырау'),
        (URALSK, u'Уральск'),
        (PAVLODAR, u'Павлодар'),
        (USKAMAN, u'Ускаман'),
        (KOKSHETAU, u'Кокшетау'),
        (TALDIK, u'Талдык'),
        (PETROPAVL, u'Петропавл'),
        (SEMEY, u'Семей'),
        (KYZYLORDA, u'Кызылорда'),
        (ZHEZKAZGAN, u'Жезказган'),
        )

    city = models.SmallIntegerField(choices=CITIES, default=0, verbose_name=u'Город')

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_moderator

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return u"{0} {1} {2}".format(self.second_name, self.first_name, self.middle_name).title()

    def __unicode__(self):
        return self.username

    def to_json(self):
        url = ''
        try:
            avatar = Avatar.objects.get(user=self)
            url = avatar.avatar.url
        except:
            # no avatar
            pass
        return {
                'id': self.pk,
                'username': self.username,
                'email': self.email, 
                'first_name':self.first_name,
                'second_name': self.second_name,
                'school': self.school,
                'city': self.city,
                'avatar': url,
                'gender': self.gender,
                'email_approved': self.email_approved
                }


class Game(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name=u'Название игры')
    
    NOT_STARTED = 0
    STARTED = 1
    FINISHED = 2

    STATUSES = (
            (NOT_STARTED, u'Не началась'),
            (STARTED, u'Началась'),
            (FINISHED, u'Закончилась')
        )

    status = models.SmallIntegerField(choices=STATUSES, default=NOT_STARTED, verbose_name=u'Статус игры')

    shuffled = models.BooleanField(default=False)

    start_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Время начала игры')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Время окончания игры')

    timestamp = models.DateTimeField(auto_now=True)

    def to_json(self):
        result = dict()
        result['name'] = self.name
        result['start_date'] = time.mktime(self.start_date.timetuple())
        result['end_date'] = time.mktime(self.end_date.timetuple())
        result['timestamp'] = time.mktime(self.timestamp.timetuple())
        return result


class GameEntry(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False, related_name='game_entries')
    player = models.ForeignKey(MainUser, blank=False, null=False, related_name='player_game_entries')
    victim = models.ForeignKey(MainUser, blank=True, null=True, related_name='victim_game_entries')

    kills = models.SmallIntegerField(default=0, verbose_name=u'Убийств')

    approved = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Секретный ключ')

    ALIVE = 0
    KILLED = 1

    STATUSES = (
            (ALIVE, u'Жив'),
            (KILLED, u'Убит')
        )

    status = models.SmallIntegerField(choices=STATUSES, default=0, verbose_name=u'Статус')
    
    timestamp = models.DateTimeField(auto_now=True)

    def to_json(self):
        result = dict()
        result['game'] = self.game.to_json()
        result['player'] = self.player.to_json()
        result['kills'] = self.kills
        result['approved'] = self.approved
        result['status'] = self.status
        if self.victim is not None:
            result['victim'] = self.victim.to_json()
        if self.secret_key is not None:
            result['secret_key'] = self.secret_key
        return result


class KillLogManager(models.Manager):

    def create_log(self, game, killer, victim):
        # TODO: push notification about new kill
        self.create(game=game, killer=killer, victim=victim)


class KillLog(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False)
    killer = models.ForeignKey(MainUser, blank=False, null=False, verbose_name=u'Убийца', related_name='killer_logs')
    victim = models.ForeignKey(MainUser, blank=False, null=False, verbose_name=u'Жертва', related_name='victim_logs')

    timestamp = models.DateTimeField(auto_now=True)

    objects = KillLogManager()

    def to_json(self):
        result = dict()
        result['game'] = self.game.to_json()
        result['killer'] = self.killer.to_json()
        result['victim'] = self.victim.to_json()
        result['timestamp'] = time.mktime(self.timestamp.timetuple())
        return result

