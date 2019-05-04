from flask import Flask, url_for, redirect, render_template, request, flash, Blueprint

lab_10 = Blueprint('lab_10', __name__, template_folder='templates')

@lab_10.route('/loginurl', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if login_check(request.form['username'], request.form['password']):
			flash('Login Success')
			user = request.form['username']
			print(user)
			return redirect(url_for('.hello', username=user))
	return render_template('login_10.html')

def login_check(username, passwd):
	if username == 'root' and passwd == 'root':
		return True
	else:
		return False

@lab_10.route('/hello/<username>')
def hello(username):
	return render_template('hello_10.html', username=username)