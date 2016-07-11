#from src.main.HmcRestClient import *
from src.utility.BaseModel import BaseModel
from peewee import *
#db = SqliteDatabase('/tmp/database.sql')
"""
db = PostgresqlDatabase(
    'hmc',  # Required by Peewee.
    user='postgres',  # Will be passed directly to psycopg2.
    password='T3mpora!',  # Ditto.
    host='127.0.0.1',  # Ditto.
)
"""
class LogicalPartition(BaseModel):
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


