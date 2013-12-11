from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse
from apps.core.forms import ImportSQLForm
from apps.core.utils import exec_sql_file
from apps.core.models import *


@login_required()
def upload(request):
    if request.method == "POST":
        form = ImportSQLForm(request.POST, request.FILES)
        if form.is_valid():
            db_name = exec_sql_file(request.user, request.FILES['import_file'])
            obj = DataBaseTmp(user=request.user, name=db_name)
            obj.save()
            return redirect(reverse(personalize, args=(obj.id,)))
    else:
        form = ImportSQLForm()
    return render(request, "upload.html", locals())


@login_required()
def personalize(request, id_db):
    if id_db:
        obj = DataBaseTmp.objects.get_or_none(id=id_db)
        return render(request, "personalize.html", locals())
    else:
        return Http404
