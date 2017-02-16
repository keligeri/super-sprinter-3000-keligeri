from peewee import *


class ConnectDatabase:

    def __init__(self):
        db_name, user_name = self.__get_connect_string()
        self.db = PostgresqlDatabase(db_name, user_name)

    def __get_connect_string(self):
        try:
            with open('connect_str.txt', "r") as f:
                details = f.readline().split(";")
                return details[0], details[1]
        except:
            print("You need to create a database and store its name in a file named 'connect_str.txt'. \
                  For more info, head over to the README")
