from peewee import *
db = SqliteDatabase("/tmp/database.sql")
class BaseModel(Model):
    class Meta:
        database = db