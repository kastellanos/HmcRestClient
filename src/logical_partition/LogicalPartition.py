from peewee import *

db = SqliteDatabase('/tmp/database.sql')

class LogicalPartition(Model):
    id = CharField()
    name = CharField()
    type = CharField()
    state = CharField()
    uuid = CharField()
    associated_managed_system = CharField()
    maximum_memory = FloatField()
    desired_memory = FloatField()
    minimum_memory = FloatField()
    has_dedicated_processors = BooleanField()
    maximum_processors = FloatField()
    desired_processors = FloatField()
    minimum_processors = FloatField()
    maximum_processing_units = FloatField()
    desired_processing_units = FloatField()
    minimum_processing_units = FloatField()

    class Meta:
        database = db
