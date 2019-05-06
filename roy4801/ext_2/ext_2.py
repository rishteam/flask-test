from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

proj_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
import config
app.config.from_object(config)

db = SQLAlchemy(app)

user_contact_relation = db.Table('user_contact_relation'
						, db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
						, db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'))
						)

class User(db.Model):
	__tabelname__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)

	# relation
	contacts = db.relationship('Contact', secondary=user_contact_relation, lazy='subquery',
                               backref=db.backref('user', lazy=True))

class Contact(db.Model):
	__tabelname__ = 'contacts'
	id = db.Column(db.Integer, primary_key=True)
	contact_style = db.Column(db.String(20))
	contact_context = db.Column(db.String(100))

db.drop_all()
db.create_all()

admin = User(username='admin')
admin_contact = Contact(contact_style='email', contact_context='admin@123.com')
admin.contacts.append(admin_contact)

db.session.add(admin)
db.session.commit()