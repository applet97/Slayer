# -*- coding: utf-8 -*-
from django.conf.urls import url
from main.views import auth, profile, process
from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', process.basic, name='main_page'),
	url(r'^login/$', auth.login, name='login'),
	url(r'^logout/$', auth.user_logout, name='logout'),
	url(r'^profile/$', profile.profile, name='profile'),
	url(r'^change_password/$', profile.change_password, name='change_password'),

]