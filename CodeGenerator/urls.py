from django.conf.urls import patterns, include, url
from apps.account.urls import account_urls as aurls
from apps.core.urls import core_urls

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^update$', 'apps.website.views.update'),
    url(r'^reload$', 'apps.website.views.reload'),
    url(r'^code/', include(core_urls)),
    url(r'^account/', include(aurls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
