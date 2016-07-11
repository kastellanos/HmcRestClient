from src.main.HmcRestClient import *
from src.utility.BaseModel import BaseModel
from peewee import *
"""
db = PostgresqlDatabase(
    'hmc',  # Required by Peewee.
    user='postgres',  # Will be passed directly to psycopg2.
    password='T3mpora!',  # Ditto.
    host='127.0.0.1',  # Ditto.
)
"""
class HardwareManagementConsole(BaseModel):
    ip = CharField()
    name = CharField()
    username = CharField()
    password = CharField()
