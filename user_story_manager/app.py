from flask import Flask, request, redirect, url_for, render_template
from user_story_manager.models import *

db = ConnectDatabase().db

app = Flask(__name__)  # create the application instance :)


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


@app.route('/')
@app.route('/list', methods=["GET"])
def show_stories():
    stories = UserStory.select().order_by(UserStory.id)
    return render_template('list.html', stories=stories)


@app.route('/story/', methods=["GET"])
def show_form():
    status_options = Status.select()
    return render_template('form.html', user_story=0, status_options=status_options, show_only=True,
                           header='Add new Story', submit_button='Create')


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
    story = UserStory.get(UserStory.id == story_id)
    status_options = Status.select()
    chosen_object = UserStory.get(UserStory.id == story_id)
    return render_template('form.html', user_story=story, status_options=status_options,
                           chosen_status=chosen_object.status, header='Edit Story', submit_button='Update')


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


@app.route('/delete/<story_id>', methods=["GET"])
def delete_story(story_id):
    story = UserStory.get(UserStory.id == story_id)
    story.delete_instance()
    story.save()
    return redirect(url_for('show_stories'))


# allow running from the command line
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
