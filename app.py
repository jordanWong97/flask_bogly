"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def show_list_users():
    """ Redirect to /users """

    return redirect('/users')

@app.get('/users')
def show_users_and_links():
    """ Show users and make them links to view user. Include add user link """

    users = User.query.all()
    return render_template('index.html', users=users)

@app.get('/users/new')
def show_add_user_form():
    """ Shows an add form for new users """

    return render_template('add_user_form.html')

@app.post('/users/new')
def process_add_form():
    """ Process the add form and add the new user. Redirect back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_information(user_id):
    """ Shows information on given user based on user_id """

    user = User.query.get(user_id) #use get_or_404 instead

    return render_template('user_page.html', user = user)

@app.get('/users/<int:user_id>/edit') #remember to put int: inside of <>
def show_edit_page(user_id):
    """ Renders template for user edit page for user """

    user = User.query.get(user_id)

    return render_template('edit_user_form.html', user = user)

@app.post('/users/<int:user_id>/edit')
def process_edit(user_id):
    """ Processes user profile update and returns to /users page """

    user = User.query.get(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    image_url = request.form['image_url']
    user.image_url = image_url if image_url else DEFAULT_IMAGE_URL  #None would make it Null instead of default

    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Deletes user """

    # user = User.query.get(user_id)
    # user.query.delete()    THIS IS ACTUALLY CALLING DELETE ON WHOLE CLASS

    User.query.filter_by(id = user_id).delete()  #this doesn't work on get

    db.session.commit()  # DONT FORGET TO COMMIT

    return redirect('/users')
