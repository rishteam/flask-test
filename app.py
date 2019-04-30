from flask import Flask, render_template, request, redirect, url_for, session, flash
from form import FormRegister
from models import Problem, Account, Submission
import datetime
from exts import db
from form import *
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import config
from flask_login import login_user, current_user, login_required, LoginManager, logout_user


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap=Bootstrap(app)
login = LoginManager(app)  
login.login_view = 'login'



@login.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

@app.route('/question_list', methods=['GET', 'POST'])
def question_list():
	return render_template('question_list.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
	return render_template('question.html')

@app.route('/submit/', methods=['GET','POST'])
@login_required
def submit():
	global submit_id
	if request.method == 'GET':
		return render_template('submit.html')
	else:
		Problem = request.form.get("problem")
		Code = request.form.get("code")
		state = Judger(Code, submit_id)
		submit_id += 1

		if state == 'AC':
			return 'Accepted'
		elif state == 'WA':
			return 'Wrong Answer'
		elif state == 'CE':
			return 'Compile Error'
		elif state == "RE":
			return 'Runtime Error'
		else:
			pass


@app.route('/')  
@login_required  
def index():
    return 'Hello Welcome My HomePage'

@app.route('/register', methods=['GET', 'POST'])
def register():
	form =FormRegister()

	if form.validate_on_submit():
		# catch time
		date_time = datetime.datetime.now()

		# user & email collision
		username = Account.query.filter(Account.username == form.username.data).first()
		email = Account.query.filter(Account.email == form.email.data).first()

		if username or email:
			return 'Username or Email collision'
		elif form.password.data != form.confirm.data:
			return 'two password is different'
		else:	
			account = Account(uid=0, username=form.username.data, nickname=form.nickname.data, password=generate_password_hash(form.password.data), email=form.email.data, permLevel=False, signUpTime=date_time, lastLoginTime=date_time, icon=False)
			db.session.add(account) 
			db.session.commit()
			flash('Success Thank You')

	return render_template('register.html', form=form)

@app.route('/test') 
def test():
	flash('flash-1')
	flash('flash-2')
	flash('flash-3')
	return render_template('index.html')  
  
  
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = FormLogin()
	if form.validate_on_submit():
		#  當使用者按下login之後，先檢核帳號是否存在系統內。
		user = Account.query.filter_by(username=form.username.data).first()
		if user:
			#  當使用者存在資料庫內再核對密碼是否正確。
			if user.check_password(form.password.data):
				login_user(user, form.remember_me.data)
				flash('Success')
				return render_template('login.html', form=form) 
			else:
				#  如果密碼驗證錯誤，就顯示錯誤訊息。
				flash('Wrong Email or Password')
		else:
			#  如果資料庫無此帳號，就顯示錯誤訊息。
			flash('Wrong Email or Password')
	return render_template('login.html', form=form) 

  
  
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('login'))
  
  
@app.route('/userinfo')  
def userinfo():  
    return 'Here is UserINFO'


if __name__ == '__main__':
    app.debug = True
    app.run()