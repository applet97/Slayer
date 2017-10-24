# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models import Count
from random import randint
import datetime, time, random, hashlib
from django.template.loader import render_to_string

from avatar.models import Avatar
from utils import random_gen

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


    def __unicode__(self):
        return self.name

    def to_json(self):
        result = dict()
        result['name'] = self.name
        result['start_date'] = time.mktime(self.start_date.timetuple())
        result['end_date'] = time.mktime(self.end_date.timetuple())
        result['timestamp'] = time.mktime(self.timestamp.timetuple())
        return result


    def shuffle_game_players(self):
        """
        """
        game_players = list(self.game_players.filter(is_active=True, is_superuser=False))
        random.shuffle(game_players)
        return game_players


    def init_game(self):
        """
        """
        players = self.shuffle_game_players()

        for i in range(0, len(players)):
            player = players[i]
            victim = players[i-1];
            game_entry, created = GameEntry.objects.get_or_create(game=self, player=player)
            game_entry.secret_key = random_gen.get_random_string(length=8)
            game_entry.victim = victim
            game_entry.save()


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
        user.is_active = True
        user.is_superuser = True
        user.is_moderator = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    """
    Model for storing main user
    """
    username = models.CharField(max_length=50, blank=False, null=False, db_index=True, unique=True, verbose_name=u'Логин',)
    email = models.EmailField(max_length=100, blank=True, verbose_name=u'email')
    email_approved = models.BooleanField(default=False, blank=True, verbose_name=u'Имейл подтвержден')

    game = models.ForeignKey(Game, blank=True, null=True, related_name='game_players')

    first_name = models.CharField(max_length=255, blank=True, verbose_name=u'Имя')
    middle_name = models.CharField(max_length=255, blank=True, verbose_name=u'Отчество')
    second_name = models.CharField(max_length=255, blank=True, verbose_name=u'Фамилия')
    school = models.CharField(max_length=100, blank=True, verbose_name=u'Школа')

    mobile_phone = models.CharField(max_length=20, blank=True, verbose_name=u'Номер телефона')


    FIT = 0
    BS = 1
    FOGI = 2
    MSHE = 3
    NOT_SELECTED = 4
    KMA = 5
    XTOB = 6
    MKM = 7
    ADMINISTRATION = 8

    FACULTIES = (
        (FIT, u'ФИТ'),
        (BS, u'БШ'),
        (FOGI, u'ФЭНГИ'),
        (MSHE, u'МШЭ'),
        (KMA, u'КМА'),
        (XTOB, u'ХТОВ'),
        (MKM, u'МКМ'),
        (ADMINISTRATION, u'Администрация'),
        )

    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    NA = 0
    
    COURSES = (
        (FIRST, u'Первый'),
        (SECOND, u'Второй'),
        (THIRD, u'Третий'),
        (FOURTH, u'Четвертый'),
        (FIFTH, u'Пятый'),
        (NA, u'N/A'),
        )

    course = models.SmallIntegerField(choices=COURSES, default=FIRST, verbose_name=u'Курс')

    faculty = models.SmallIntegerField(choices=FACULTIES, default=NOT_SELECTED, verbose_name=u'Факультет')
    
    birth_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата рождения')

    is_active = models.BooleanField(default=True)
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
        return self.username + " " + self.first_name + " " + self.second_name

    def to_json(self):
        url = ''
        try:
            avatar = Avatar.objects.get(user=self)
            url = avatar.avatar.url
        except:
            # no avatar
            pass
            
        return {
                'username': self.username,
                'first_name':self.first_name,
                'second_name': self.second_name,
                'course': self.course,
                'faculty': self.faculty,
                'avatar': url,
                }



class GameEntryManager(models.Manager):
    
    def create_game_entry(self, player, victim):
        """
        """        
        game_entry = self.create(player=player, victim=victim)
        game_entry.secret_key = "a";
        game_entry.save()
        return game_entry


class GameEntry(models.Model):
    game = models.ForeignKey('Game', blank=False, null=False, related_name='game_entries')
    player = models.ForeignKey('MainUser', blank=False, null=False, related_name='player_game_entries')
    victim = models.ForeignKey('MainUser', blank=True, null=True, related_name='victim_game_entries')

    kills = models.SmallIntegerField(default=0, verbose_name=u'Убийств')

    approved = models.BooleanField(default=True)
    secret_key = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Секретный ключ')
    is_active = models.BooleanField(default=True, verbose_name=u"Активно")
    timestamp = models.DateTimeField(auto_now=True)

    ALIVE = 0
    KILLED = 1
    
    STATUSES = (
            (ALIVE, u'Жив'),
            (KILLED, u'Убит')
        )

    status = models.SmallIntegerField(choices=STATUSES, default=0, verbose_name=u'Статус')

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

    def __unicode__(self):
        return self.game.__unicode__() + " " + self.player.__unicode__() + " vs " + self.victim.__unicode__()

    class Meta:
        unique_together = ('game', 'player',)
        verbose_name_plural = u'Game Entries'
        ordering = ['-is_active']


class KillLogManager(models.Manager):

    def create_log(self, entry):
        # TODO: push notification about new kill
        log = self.create(game=entry.game, killer=entry.player, victim=entry.victim)
        return log


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

    def __unicode__(self):
        return self.game.__unicode__() + " " + self.killer.__unicode__()
