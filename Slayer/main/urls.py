# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from main.views import auth, profile, process, game
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings	


urlpatterns = [
	url(r'^$', process.basic, name='main_page'),
	url(r'^avatar/', include('avatar.urls')),
	url(r'^login/$', auth.login, name='login'),
	url(r'^logout/$', auth.user_logout, name='logout'),
	url(r'^profile/$', profile.profile, name='profile'),
	url(r'^change_password/$', profile.change_password, name='change_password'),
	url(r'^search/$', profile.search, name='search'),
	url(r'^rating/$', process.rating, name='rating'),
	url(r'^history/$', process.history, name='history'),
	url(r'^kill/$', game.kill, name="kill"),

	url(r'^avatar/', include('avatar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)