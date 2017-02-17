from flask import Flask, request, redirect, url_for, render_template, g
from user_story_manager.models import *

# config - aside from our database, the rest is for use by Flask
db = ConnectDatabase().db
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flask.py


def init_db():
    db.connect()
    if UserStory.table_exists():
        UserStory.drop_table(cascade=True)
        db.create_table(UserStory, safe=True)

    else:
        db.create_table(UserStory, safe=True)

    if Status.table_exists():
        Status.drop_table(cascade=True)
        db.create_table(Status, safe=True)
        update_status_table()

    else:
        db.create_table(Status, safe=True)
        update_status_table()


def update_status_table():
    status_list = ['Planning', 'To Do', 'In Progress', 'Review', 'Done']
    for status in status_list:
        new_status = Status.create(status_options=status)
        new_status.save()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print ("Initialized the database")

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()

@app.route('/story/', methods=["GET"])
def show_form():
    story = []      # ez nem hiszem h kéne
    status_options = Status.select()
    return render_template('form.html', user_story=0, status_options=status_options, show_only=True, header='Add new Story', submit_button='Create')

@app.route('/story/', methods=["POST"])
def add_new_story():
    new_story = UserStory.create(title=request.form['story_title'],
                                 story=request.form['user_story'],
                                 criteria=request.form['acceptance_criteria'],
                                 business_value=request.form['business_value'],
                                 estimation=request.form['estimation'],
                                 status=request.form['status'])
    new_story.save()
    return redirect(url_for('show_stories'))

@app.route('/story/<story_id>', methods=["GET"])
def show_edit_story(story_id):
    stories = UserStory.get(UserStory.id == story_id)
    status_options = Status.select()
    status = UserStory.get(UserStory.id == story_id)
    return render_template('form.html', user_story=stories, status_options=status_options, chosen_status=status.status, header='Edit Story', submit_button='Update')

@app.route('/story/<story_id>', methods=["POST"])
def edit_story(story_id):
    editing_story = UserStory.update(title=request.form['story_title'],
                                 story=request.form['user_story'],
                                 criteria=request.form['acceptance_criteria'],
                                 business_value=request.form['business_value'],
                                 estimation=request.form['estimation'],
                                 status=request.form['status']).where(UserStory.id == int(story_id))
    editing_story.execute()
    return redirect(url_for('show_stories'))

@app.route('/')
@app.route('/list', methods=["GET"])
def show_stories():
    stories = UserStory.select().order_by(UserStory.id)
    return render_template('list.html', stories=stories)



# allow running from the command line
if __name__ == '__main__':
    init_db()
    app.run(debug=True)