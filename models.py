"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = 'https://tinyurl.com/2p86tjer'  #put something here instead of NONE

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.String,
                    default = DEFAULT_IMAGE_URL,
                    nullable=False)

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                    default=datetime.utcnow, #sqlalchemy.sql.functions.current_timestamp
                    nullable=False)
    user_id = db.Column(db.Integer,
                   db.ForeignKey('users.id'))
    author = db.relationship('User',
                    backref = 'posts')

