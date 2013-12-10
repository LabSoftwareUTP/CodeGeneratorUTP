from django.shortcuts import render
from apps.core.forms import ImportSQLForm
from apps.core.utils import exec_sql_file


def upload(request):
    if request.method == "POST":
        form = ImportSQLForm(request.POST, request.FILES)
        if form.is_valid():
            exec_sql_file(request.user, request.FILES['import_file'])
    else:
        form = ImportSQLForm()
    return render(request, "upload.html", locals())
