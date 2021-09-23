from peewee import *
from os import path
database_path = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(database_path, "MyDatabase.db"))

class Users(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
Users.create_table(fail_silently=True)

class Booking(Model):
    name = CharField()
    nationality = CharField()
    current_residence = CharField()
    county = CharField()
    constituency = CharField()
    address = CharField()
    phone_no = IntegerField()
    email = CharField(unique=True)
    service_needed = CharField()
    venue = CharField()
    date = DateField()
    time = TimeField()
    capacity = IntegerField()
    description = TextField()

    class Meta:
        database = db
Booking.create_table(fail_silently=True)