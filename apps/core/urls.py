from django.conf.urls import patterns, url

general_urls = patterns('apps.core.views',
    url(r'^upload$', 'upload', name="upload"),
    url(r'^database/(?P<id_db>[0-9]+)/$', 'personalize', name="personalize"),
)

sql_urls = patterns('apps.core.views',
    url(r'^db/(?P<id_db>[0-9]+)/del-table/(?P<table_name>[\w]+)$', 'delete_table', name="del_table"),
)

core_urls = general_urls + sql_urls