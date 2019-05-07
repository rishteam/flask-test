from flask import Flask, render_template
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

import os

proj_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
import config
app.config.from_object(config)

class UserReigsterForm(FlaskForm):
	username = StringField('UserName', validators=[DataRequired(message='不能為空')])
	email = EmailField('Email', validators=[DataRequired(message='不能為空')])
	submit = SubmitField('送出')

@app.route('/register', methods=['GET', 'POST'])
def user_register():
	form = UserReigsterForm()

	if form.validate_on_submit():
		return 'Success Submit'
	return render_template('register.html', form=form)


if __name__ == "__main__":
	app.run(host='0.0.0.0')