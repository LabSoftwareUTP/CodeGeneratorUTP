from django.conf.urls import patterns, url

general_urls = patterns('apps.core.views',
    url(r'^upload$', 'upload', name="upload"),
    url(r'^personalize/(?P<id_db>[0-9]+)/$', 'personalize', name="personalize"),
)
core_urls = general_urls