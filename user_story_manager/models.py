from peewee import *
from user_story_manager.connect_database import ConnectDatabase

class UserStory(Model):
    title = CharField()
    story = CharField()
    criteria = CharField()
    business_value = IntegerField(constraints=[Check('business_value >= 100 and business_value <= 1500')])
    estimation = DecimalField(constraints=[Check('estimation >= 0.5 and estimation <= 40')])
    status = CharField(constraints=[Check("status = 'Planning' or status = 'To Do' or status = 'In Progress'\
    or status = 'Review' or status = 'Done'")])

    class Meta:
        database = ConnectDatabase().db
        # constraints=[Check('business_value % 100 == 0' and 'business_value >= 100' and 'business_value <= 1500')]
        # constraints=[Check('status == Planning' or 'status == To Do' or 'status == In Progress' or 'status == Review' or 'status == Done')]
        # [Check('estimation >= 0.5' and 'estimation <= 40')]