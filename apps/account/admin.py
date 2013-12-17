from django.contrib import admin
from django.db.models import get_app, get_models

app = get_app('account')

for model in get_models(app):
	admin.site.register(model)
