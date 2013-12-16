from django.conf.urls import patterns, url

general_urls = patterns('apps.core.views',
    url(r'^upload$', 'upload', name="upload"),
    url(r'^db/(?P<id_db>[0-9]+)/$', 'personalize', name="personalize"),
)

sql_urls = patterns('apps.core.views',
    url(r'^db/(?P<id_db>[0-9]+)/del-table/(?P<table_name>[\w]+)$', 'delete_table', name="del_table"),
    url(r'^db/(?P<id_db>[0-9]+)/update-table-name/$', 'update_table_name', name="update_table_name"),
    url(r'^db/(?P<id_db>[0-9]+)/inspectdb/$', 'inspectdb', name="inspectdb"),
)

core_urls = general_urls + sql_urls