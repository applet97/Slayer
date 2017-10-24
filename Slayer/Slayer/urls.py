from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^jet/', include('jet.urls', 'jet')),
	url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('main.urls', namespace='main')),
    #url(r'^moderators/', include('moderators.urls', namespace='moderators')),
    url(r'^api/', include('main.urls', namespace='api')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
