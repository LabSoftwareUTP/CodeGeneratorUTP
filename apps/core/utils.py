
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


def create_db(user):
    db1 = MySQLdb.connect(host="localhost",user=DB_USER,passwd=DB_USER_PASSWD)
    cursor = db1.cursor()
    db_name = 'tmp_db_%s_%s' % (user.username, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M"))
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
            else:
                print "NO SE EJECUTO: %s..." % statement[0:20]
            statement = ""
    return db_temp, path


import commands
from django.template.defaultfilters import slugify
from apps.inspectdb.management.commands import inspectdb
import zipfile

def create_app(user, app_name, db_name):
    app_name = slugify(app_name)
    app_path = "%s/%s/%s" % (settings.MEDIA_ROOT, str(user.id) + "-" + user.username, app_name)
    #we need to have another database in the settings var to use inspectdb
    settings.DATABASES['mysql'] = {'ENGINE': 'django.db.backends.mysql','NAME': db_name,'USER': DB_USER,'PASSWORD': DB_USER_PASSWD}
    
    print "Creando app en %s" % app_path
    commands.getoutput("mkdir %s" % app_path)
    init = open("%s/__init__.py" % app_path, "w")
    init.close()

    text = "from django.conf.urls import patterns, url\n\ngeneral_urls = patterns('%s.views',\n\turl(r'^$', 'home', name='%s_home'),\n)" % (app_name, app_name)
    urls = open("%s/urls.py" % app_path, "w")
    urls.write(text)
    urls.close()
    
    views = open("%s/views.py" % app_path, "w")
    text = "# encoding:utf-8\nfrom django.shortcuts import render\n\ndef home(request):\n\treturn render(request, 'index.html', locals())\n"
    views.write(text)
    views.close()

    models = open("%s/models.py" % app_path, "w")
    inspectdb.Command().execute(stdout=models)
    models.close()
    commands.getoutput("mkdir %s/templates" % app_path)
    commands.getoutput("cp %s/apps/core/app_templates/* %s/templates/" % (settings.BASE_DIR, app_path))
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
