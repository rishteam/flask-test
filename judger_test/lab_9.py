from flask import Flask, url_for, redirect, render_template, request, flash, Blueprint

lab_9 = Blueprint('lab_9', __name__, template_folder='templates')

@lab_9.route('/loginurl', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return redirect(url_for('lab_9.hello', username=request.form.get('username')))
	return render_template('login_9.html')

@lab_9.route('/hello/<username>')
def hello(username):
	return render_template('hello_9.html', username=username)
