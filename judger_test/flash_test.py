from flask import Flask, url_for, redirect, render_template, request, flash, Blueprint, session

flash_test = Blueprint('flash_test', __name__, template_folder='templates')

@flash_test.route('/flash')
@flash_test.route('/flash/<s>')
def flash_h(s=None):
	if s:
		flash(s)
	return render_template('flash_test.html')