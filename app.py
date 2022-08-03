"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    """ Lists and shows users """

    users = User.query.all()
    return render_template('index.html', users = users)

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