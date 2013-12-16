import MySQLdb
from _mysql_exceptions import OperationalError, ProgrammingError, IntegrityError
from django.conf import settings
DB_USER = settings.MYSQL_USER
DB_USER_PASSWD = settings.MYSQL_PASSWD


class DataBase():
    
    def __init__(self, **kwargs):
        try:
            db = MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_USER_PASSWD, db=kwargs['name'])
            self.cursor = db.cursor()
            self.db = kwargs['name']
        except (OperationalError, ProgrammingError) as e:
            print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            # return None
            # raise e

    def show_tables(self):
        try:
            self.cursor.execute("SHOW TABLES;")
            return self.cursor.fetchall()
        except (OperationalError, ProgrammingError) as e:
            print "\n[WARN show_tables] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            return None

    def delete_db(self):
        try:
            self.cursor.execute("DROP DATABASE %s;" % self.db)
            return self.cursor.fetchall()
        except (OperationalError, ProgrammingError) as e:
            print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            return None

    def delete_table(self, table=None):
        if table:
            sql = "DROP TABLE IF EXISTS %s CASCADE;" % table
            try:
                print sql
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
                return None
            except IntegrityError, e:
                print "\n[IntegrityError]", e
                return None
        else:
            return None

    def rename_table(self, old_name=None, new_name=None):
        if old_name and new_name:
            sql = "RENAME TABLE %s TO %s;" % (old_name, new_name)
            try:
                print sql
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
                return {"error": "[WARN] MySQLError during execute statement: Args: '%s'" % (str(e.args))}
        else:
            return {}

    def show_fields(self, table=None):
        if table:
            try:
                self.cursor.execute("DESCRIBE %s;" % table)
                return self.cursor.fetchall()
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
                return None
        else:
            return None
