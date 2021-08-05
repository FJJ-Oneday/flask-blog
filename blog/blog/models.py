from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

from datetime import datetime
from flask_login import UserMixin
import hashlib

from bs4 import BeautifulSoup


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(255), default='')
    password_hash = db.Column(db.String(255), default='')

    posts = db.relationship('Post', back_populates='user', cascade='all')

    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return '<user ' + self.name + '>'

    @property
    def password(self):
        return '不可读字段'

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def email_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)

    posts = db.relationship('Post', back_populates='category')

    def __repr__(self):
        return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), default='', index=True)
    body = db.Column(db.Text, default='')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates="posts")

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    comments = db.relationship('Comment', back_populates='post')

    @property
    def text(self):
        soup = BeautifulSoup(self.body)
        return soup.get_text()

    def __repr__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    is_root = db.Column(db.Boolean, default=True)
    is_reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='comments')
