from src.main.HmcRestClient import *

from peewee import *
db = SqliteDatabase('/tmp/database.sql')
class HardwareManagementConsole(Model):
    ip = CharField()
    name = CharField()
    username = CharField()
    password = CharField()

    class Meta:
        database = db