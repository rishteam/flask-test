from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

proj_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
import config
app.config.from_object(config)

db = SQLAlchemy(app)

class User(db.Model):
	__tabelname__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __init__(self, username, email, **kwargs):
		super().__init__(**kwargs)
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def __str__(self):
		info = self.__repr__() + ' '
		info += self.email
		return info

def add_user():
	admin = User('admin', 'admin@123.com')
	user1 = User('user1', 'user1@123.com')

	db.session.add(admin)
	db.session.add(user1)
	db.session.commit()

def query_all():
	all_users = User.query.all()
	print(all_users)

def search_user(**kwargs):
	return User.query.filter_by(**kwargs)

def delete_user(username):
	target = search_user(username=username).first()

	if target:
		db.session.delete(target)
		db.session.commit()

def update_user(user, username=None, email=None):
	if username:
		user.username = username
	if email:
		user.email = email
	db.session.add(user)
	db.session.commit()

print(type(User.query.first()))

# u = search_user(username='user1')
# print(u.first())
# update_user(u.first(), '123', '456')