import os
from peewee import *
from connect_database import ConnectDatabase
from models import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, current_app

# config - aside from our database, the rest is for use by Flask
db = ConnectDatabase().db
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flask.py


def drop_table():
    db.connect()
    if UserStory.table_exists():
        UserStory.drop_table(cascade=True)


def create_tables():
    db.connect()
    db.create_table(UserStory, safe=True)

@app.route('/', methods=["GET"])
def show_form():
    return render_template('form.html')

@app.route('/story', methods=["GET","POST"])
def add_new_story():
    if request.method == 'POST':
        with db.transaction():
            new_story = UserStory.create(title=request.form['story_title'],
                                         story= request.form['user_story'],
                                         criteria= request.form['acceptance_criteria'],
                                         business_value=request.form['business_value'],
                                         estimation=request.form['estimation'],
                                         status=request.form['status'])
            new_story.save()
        return redirect(url_for('show_stories'))

    return render_template('form.html')

@app.route('/story/story_id', methods=["POST"])
def edit_story():
    pass

@app.route('/list', methods=["GET"])
def show_stories():
    stories = UserStory.select().order_by(UserStory.id)
    return render_template('list.html', stories=stories)

# allow running from the command line
if __name__ == '__main__':
    app.run()