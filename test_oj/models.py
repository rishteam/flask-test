from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin


# build the tables
class Problem(db.Model):
	__tablename__  = 'problem'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	uid = db.Column(db.Integer, primary_key=True , nullable=False, unique=True)
	problemName = db.Column(db.String(100), nullable=False, unique=True)
	problemId = db.Column(db.Integer, nullable=False, unique=True)

class Account(UserMixin, db.Model):
	__tablename__  = 'account'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	uid = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	nickname = db.Column(db.String(30), nullable=False, unique=False)
	password = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	permLevel = db.Column(db.Integer, nullable=False)
	signUpTime = db.Column(db.DateTime, nullable=False) # 註冊時間
	lastLoginTime = db.Column(db.DateTime, nullable=False) # 最後登入時間
	icon = db.Column(db.Boolean, nullable=False) # 保留給頭像用


	def check_password(self, password):
		return check_password_hash(self.password, password)

	def get_id(self):
		return self.uid

	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def is_anoymous(self):
		return False


class Account_valid(db.Model):
	__tablename__ = 'account_valid'
	uid = db.Column(db.Integer, primary_key=True, unique=True)

class Submission(db.Model):
	__tablename__  = 'submission'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	uid = db.Column(db.Integer, primary_key=True, nullable=False)# 提交題號
	result = db.Column(db.String(10), nullable=False)# 結果
	resTime = db.Column(db.Float, nullable=False)# 執行時間
	resMem = db.Column(db.Float, nullable=False)# 執行記憶體
	code = db.Column(db.Text, nullable=False)# 程式碼長度
	lang = db.Column(db.String(10), nullable=False)# 語言
	rank = db.Column(db.Integer, nullable=False)# 排名
	time = db.Column(db.DateTime, nullable=False)# 繳交時間



