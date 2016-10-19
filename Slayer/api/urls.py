from django.conf.urls import patterns,url
from api.views import auth, game

urlpatterns = [
    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^register/$', auth.register, name='register'),
    url(r'^forgot_password/$', auth.forgot_password, name='forgot_password'),

    url(r'^game/register/$', game.register, name='game_register'),
]