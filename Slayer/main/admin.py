# -*- coding: utf-8 -*-
import ast

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import MainUser
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