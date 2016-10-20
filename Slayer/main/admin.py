# -*- coding: utf-8 -*-
import ast

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import MainUser, Game, GameEntry, KillLog
from main.forms import MainUserCreationForm, MainUserChangeForm

@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    form = MainUserChangeForm

    add_form = MainUserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'id',
        'username',
        'email',
        'email_approved',
        'first_name',
        'is_moderator',
        'city',
        'is_active',
        'gender',
    )

    list_filter = ('is_moderator', )

    search_fields = ['username', 'email', 'first_name', 'second_name']

    fieldsets = (
        (None, {'fields' : (
                    'username',
                    'email',
                    'first_name',
                    'middle_name',
                    'second_name',
                    'mobile_phone',
                    'faculty',
                    'birth_date',
                    'gender',
            )}),
        ('Password', {'fields' : ('password', ) }),  # we can change password in admin-site
        ('Permissions', {'fields' : ('is_active',  'is_moderator', 'is_superuser',  ) }),
    )


    add_fieldsets = (
        (None, {'fields' : ('username', 'password1', 'password2') }),
        ('Permissions', {'fields' : ('is_active', 'is_superuser', ) }),
    )

    ordering = ('username',)
    filter_horizontal = ()


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'shuffled',
        'start_date',
        'end_date'
    )


@admin.register(GameEntry)
class GameEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'game',
        'player',
        'victim',
        'kills',
        'approved',
        'secret_key',
        'status'
    )


@admin.register(KillLog)
class KillLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'game',
        'killer',
        'victim'
    )
    