from peewee import *
from user_story_manager.connect_database import ConnectDatabase


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = ConnectDatabase().db


class UserStory(BaseModel):
    title = CharField()
    story = CharField()
    criteria = CharField()
    business_value = IntegerField(constraints=[Check('business_value >= 100 and business_value <= 1500')])
    estimation = DecimalField(constraints=[Check('estimation >= 0.5 and estimation <= 40')])
    status = CharField()


class Status(BaseModel):
    status_options = CharField()
