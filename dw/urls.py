from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from dwApp.views import index, htweets, users, etweets, gtweets, about


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^htweets$', htweets, name='ht'),
                       url(r'^etweets$', etweets, name='et'),
                       url(r'^tweets/(.*)$', gtweets, name='gt'),
                       url(r'^users$', users, name='usr')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)