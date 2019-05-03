from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, session

lab_11 = Blueprint('lab_11', __name__, template_folder='lab_11')

@lab_11.route('/login_inherit', methods=['GET', 'POST'])
def login_inherit():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		flash('{} {}'.format(request.form['username'], request.form['password']))
	return render_template('login_inherit.html')