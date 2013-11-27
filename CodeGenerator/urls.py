from django.conf.urls import patterns, include, url
from apps.account.urls import account_urls as aurls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^account/', include(aurls)),
    url(r'^admin/', include(admin.site.urls)),
)
