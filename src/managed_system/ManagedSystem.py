from peewee import *
from src.utility.BaseModel import BaseModel
"""
db = PostgresqlDatabase(
    'hmc',  # Required by Peewee.
    user='postgres',  # Will be passed directly to psycopg2.
    password='T3mpora!',  # Ditto.
    host='127.0.0.1',  # Ditto.
)
"""
class ManagedSystem(BaseModel):
    id = CharField()
    name = CharField()
    machine_type = CharField()
    model = CharField()
    associated_hmc = CharField()
