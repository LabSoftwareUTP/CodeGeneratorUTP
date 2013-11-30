from django.conf.urls import patterns, url

general_urls = patterns('apps.account.views',
    url(r'^$', 'personal_data', name="personal_data"),
    url(r'^new', 'newUser', name="new_user"),
    url(r'^edit$', 'update_personal_data', name="update_personal_data"),
    url(r'^changePassword', 'changePassword', name="change_password"),
    url(r'^password/reset/$', 'password_reset2', name="password_reset2"),
    url(r'^password/reset/done/$', 'password_reset_done2', name="password_reset_done2"),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm2', name="password_reset_confirm2"),
    url(r'^password/done/$', 'password_reset_complete2', name="password_reset_complete2"),
    url(r'^activate/(?P<activation_key>[-\w]+)/invited(?P<is_invited>.*)', 'confirm_account', name="confirm_account"),
    url(r'^activate/(?P<activation_key>[-\w]+)', 'activate_account', name="activate_account"),
    url(r'^login', 'log_in', name="login"),
    url(r'^logout', 'log_out', name="logout"),
)
users = patterns('apps.account.views',
    url(r'^lista-de-usuarios/$', 'admin_users', name="admin_users"),
    url(r'^editar-usuario/(?P<id_user>[0-9]+)/$', 'update_user', name="update_user"),
    url(r'^eliminar-usuario/(?P<id_user>[0-9]+)/$', 'delete_user', name="delete_user"),
    url(r'^ver-usuario/(?P<id_user>[0-9]+)/$', 'read_user', name="read_user"),
    url(r'^asignar-credenciales/(?P<id_user>[0-9]+)/$', 'permission_login', name="permission_login"),
)
account_urls = general_urls + users