from django.conf.urls import patterns, include, url
from apps.account.urls import account_urls as aurls
from apps.core.urls import core_urls
from djangosql.urls import general_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^code/', include(core_urls)),
    url(r'^djangosql/', include(general_urls, namespace='djangosql')),
    url(r'^account/', include(aurls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
