# -*- coding: utf-8 -*-
import ast

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import MainUser, Game, GameEntry, KillLog
from main.forms import MainUserCreationForm, MainUserChangeForm

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from avatar.models import Avatar


class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 1

@admin.register(MainUser)
class MainUserAdmin(UserAdmin):

    inlines = [
        AvatarInline
    ]

    form = MainUserChangeForm

    add_form = MainUserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username',
        'first_name',
        'second_name',
        'faculty',
        'course',
        'game',
        'is_active',
        'is_superuser',
    )

    list_filter = ('is_moderator', )

    search_fields = ['username', 'email', 'first_name', 'second_name']

    fieldsets = (
        (None, {'fields' : (
                    'username',
                    'game',
                    'email',
                    'first_name',
                    'second_name',
                    'mobile_phone',
                    'faculty',
                    'course',
            )}),
        ('Password', {'fields' : ('password', ) }),  # we can change password in admin-site
        ('Permissions', {'fields' : ('is_active',  'is_moderator', 'is_superuser',  ) }),
    )


    add_fieldsets = (
        (None, {'fields' : ('username', 'password1', 'password2', 'game', 
                'first_name', 'second_name', 'faculty', 'course') }),
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
        'end_date',
    )




@admin.register(GameEntry)
class GameEntryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'player',
        'victim',
        'status',
        'kills',
        'game',
        'secret_key',
        'is_active',
    )

    list_filter = ('status', )

    ordering = ('status', '-kills')


@admin.register(KillLog)
class KillLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'game',
        'killer',
        'victim',
        'timestamp'
    )
    

admin.site.site_header = 'Slayer administration'