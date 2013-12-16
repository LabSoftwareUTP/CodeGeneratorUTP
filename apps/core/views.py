# encoding:utf-8
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings
import json
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
        if obj:
            conn = DataBase(name=obj.db_name) #connection
            tables = []
            for t in conn.show_tables():
                tables.append({"name": t, "columns": conn.show_fields(table=t)})
            return render(request, "personalize.html", locals())
        else:
            raise Http404
    else:
        raise Http404


@login_required()
def delete_table(request, id_db, table_name):
    if id_db and table_name:
        obj = DataBaseTmp.objects.get_or_none(id=id_db)
        if obj:
            conn = DataBase(name=obj.db_name) #connection
            conn.delete_table(table=table_name)
            return redirect(reverse(personalize, args=(obj.id,)))
        else:
            raise Http404
    else:
        raise Http404


@login_required()
def inspectdb(request, id_db):
    if id_db:
        obj = DataBaseTmp.objects.get_or_none(id=id_db)
        if obj:
            create_app(request.user, obj.filename, obj.db_name)
            return redirect(reverse(personalize, args=(obj.id,)))
        else:
            raise Http404
    else:
        raise Http404


@login_required()
def update_table_name(request, id_db):
    if request.is_ajax() and id_db:
        if request.method == "POST":
            old_name = request.POST.get("old_name") if "old_name" in request.POST else False
            new_name = request.POST.get("new_name") if "new_name" in request.POST else False
            if old_name and new_name:
                obj = DataBaseTmp.objects.get_or_none(id=id_db)
                if obj:
                    conn = DataBase(name=obj.db_name) #connection
                    r = conn.rename_table(old_name=old_name, new_name=new_name)
                    if "error" in r:
                        response = {"error": r['error']}
                    else:
                        response = {"saved": True}
                else:
                    response = {"error": _("Error, la base de datos no existe")}
            else:
                response = {"error": _("Error, no hay un nombre para cambiar")}
        else:
            response = {"error": _(u"No es posible servir esta petición")}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404
