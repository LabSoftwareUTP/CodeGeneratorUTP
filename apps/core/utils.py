
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from _mysql_exceptions import OperationalError, ProgrammingError, IntegrityError
import os
import re
import MySQLdb
import datetime


def exec_sql_file(user, sql_file):
    """Thanks to @noumenon for his code: http://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb"""
    
    db_temp = "temp"
    db = MySQLdb.connect(user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD, db=db_temp)

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
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                db.cursor().execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            except IntegrityError, e:
                print "YA EXISTE ESA TABLA"

            statement = ""