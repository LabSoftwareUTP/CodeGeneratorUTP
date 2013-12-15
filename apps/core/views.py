from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse
from apps.core.forms import ImportSQLForm
from apps.core.models import *
from apps.core.utils import *


@login_required()
def upload(request):
    if request.method == "POST":
        form = ImportSQLForm(request.POST, request.FILES)
        if form.is_valid():
            db_name, media_filename = exec_sql_file(request.user, request.FILES['import_file'])
            obj = DataBaseTmp(user=request.user, db_name=db_name, filename=request.FILES['import_file'].name, media_filename=media_filename)
            obj.save()
            return redirect(reverse(personalize, args=(obj.id,)))
    else:
        form = ImportSQLForm()
    return render(request, "upload.html", locals())


@login_required()
def personalize(request, id_db):
    if id_db:
        obj = DataBaseTmp.objects.get_or_none(id=id_db)
        conn = DataBase(name=obj.db_name) #connection
        tables = []
        for t in conn.show_tables():
            tables.append({"name": t, "columns": conn.show_fields(table=t)})
        return render(request, "personalize.html", locals())
    else:
        return Http404
