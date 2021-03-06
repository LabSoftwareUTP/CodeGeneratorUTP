
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from _mysql_exceptions import OperationalError, ProgrammingError, IntegrityError
import os
import re
import MySQLdb
import datetime
DB_USER = settings.MYSQL_USER
DB_USER_PASSWD = settings.MYSQL_PASSWD



VIEW_TEMPLATE = '''# encoding:utf-8
from django.shortcuts import render
def home(request):
    app_name = '{app_name}'
    return render(request, '{app_name}/index.html', locals())

'''


def sformat(cad, **kw):
    return cad.format(**kw)

def create_db(user):
    db1 = MySQLdb.connect(host="localhost",user=DB_USER,passwd=DB_USER_PASSWD)
    cursor = db1.cursor()
    db_name = 'tmp_db_%s_%s' % (user.username, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%s"))
    sql = "CREATE DATABASE %s;" % (db_name)
    try:
        cursor.execute(sql)
    except Exception, e:
        raise e
    return db_name


def exec_sql_file(user, sql_file):
    """Thanks to @noumenon for his code: http://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb"""
    
    db_temp = create_db(user)
    db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_USER_PASSWD, db=db_temp)

    filename = '%s/%s-%s' % (str(user.id) + "-" + user.username, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"), sql_file.name)
    path = default_storage.save(filename, ContentFile(sql_file.read()))
    sql_file = os.path.join(settings.MEDIA_ROOT, path)

    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            # if statement[0:11] != "CREATE TABLE":
            if re.search(r'CREATE TABLE', statement):
                print "SQL: %s...\n" % statement[0:20]
                try:
                    db.cursor().execute(statement)
                except (OperationalError, ProgrammingError) as e:
                    print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
                except IntegrityError, e:
                    print "YA EXISTE ESA TABLA", e
            # else:
            #     print "NO SE EJECUTO: %s..." % statement[0:20]
            statement = ""
    return db_temp, path


import commands
from django.template.defaultfilters import slugify
from apps.inspectdb.management.commands import inspectdb
import zipfile


def fnc(name):
    x = open(name,'r').read()
    x = x.replace("=0L", "=1L")
    with open(name,'w') as f:
        f.write(x)


def create_app(user, app_name, db_name):
    app_name = slugify(app_name)
    app_path = "%s/%s/%s" % (settings.MEDIA_ROOT, str(user.id) + "-" + user.username, app_name)
    #we need to have another database in the settings var to use inspectdb
    settings.DATABASES['mysql'] = {'ENGINE': 'django.db.backends.mysql','NAME': db_name,'USER': DB_USER,'PASSWORD': DB_USER_PASSWD}
    
    print "Creando app en %s" % app_path
    commands.getoutput("mkdir -p %s" % app_path)
    init = open("%s/__init__.py" % app_path, "w")
    init.close()

    text = "from django.conf.urls import patterns, url\n\ngeneral_urls = patterns('%s.views',\n\turl(r'^$', 'home', name='%s_home'),\n)" % (app_name, app_name)
    urls = open("%s/urls.py" % app_path, "w")
    urls.write(text)
    urls.close()
    
    views = open("%s/views.py" % app_path, "w")
    text = sformat(VIEW_TEMPLATE,app_name=app_name)
    views.write(text)
    views.close()

    models = open("%s/models.py" % app_path, "w")
    inspectdb.Command().execute(stdout=models)
    models.close()
    fnc("%s/models.py" % app_path)

    readme = open("%s/admin.py" % app_path, "w")
    text = u"from django.contrib import admin\nfrom django.db.models import get_app, get_models \n\napp = get_app('%s') \n\nfor model in get_models(app): \n\tadmin.site.register(model)" % (app_name)
    readme.write(text)
    readme.close()

    readme = open("%s/README.MD" % app_path, "w")
    text = u"#Instalation\n\nadd `{appname}` to your INSTALED_APPS var\n\nadd to you urls:\n\n\tfrom {appname}.urls import general_urls as {appname}_urls\n\n\t...\n\n\turl(r'^{appname}/', include({appname}_urls)),\n\n\nThen, now you can to sync your proyect\n\n\tpython manage.py syncdb".format(appname=app_name)
    readme.write(text)
    readme.close()
    orden= "mkdir -p {apppath}/templates/{appname} ".format(apppath=app_path,appname=app_name)
    print orden
    commands.getoutput(orden)
    copiar = "cp {base}/apps/core/app_templates/* {apppath}/templates/{appname}".format(base=settings.BASE_DIR, apppath=app_path, appname=app_name)
    print copiar
    commands.getoutput(copiar)

    zip_app = compress_app(app_path, app_name, zfilename=app_name + ".zip")

    return  "%s-%s/%s.zip" % (str(user.id), user.username, app_name)


def compress_app(app_path, app_name, zfilename='default.zip'): # 
    zipf = zipfile.ZipFile(app_path + "/../" + zfilename, 'w', zipfile.ZIP_DEFLATED)
    zipdir(app_path , zipf)
    zipf.close()
    return zipf


def zipdir(dir_path, zip):
    for root, dirs, files in os.walk(dir_path):
        # print "root: %s\ndirs: %s\nfiles: %s" % (root, dirs, files)
        zip.write(root)
        for file in files:
            zip.write(os.path.join(root, file))
