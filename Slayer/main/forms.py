# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from main.models import MainUser
from django.forms import ModelForm

User = get_user_model()


class MainUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MainUserCreationForm, self).__init__(*args, **kwargs)
        #del self.fields['username'] # remove username field that was inherited from AbstractBaseUser

    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
        exclude = [
        ]