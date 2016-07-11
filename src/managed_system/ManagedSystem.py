from peewee import *
from src.main.HmcRestClient import *
db = SqliteDatabase('/tmp/database.sql')
class ManagedSystem(Model):
    id = CharField()
    name = CharField()
    machine_type = CharField()
    model = CharField()
    associated_hmc = CharField()

    class Meta:
        database = db