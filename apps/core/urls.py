from django.conf.urls import patterns, url

general_urls = patterns('apps.core.views',
    url(r'^upload$', 'upload', name="upload"),
)
core_urls = general_urls