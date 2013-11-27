from django.conf.urls import patterns, url

account_urls = patterns('apps.account.views',
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
