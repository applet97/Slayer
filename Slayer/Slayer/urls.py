from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('main.urls', namespace='main')),
    #url(r'^moderators/', include('moderators.urls', namespace='moderators')),
    #url(r'^api/', include('api.urls', namespace='api')),
]
