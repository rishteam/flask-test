import sys
sys.path.append('./judger/')

from flask import Flask, url_for, redirect, render_template, request
import config

import judge

app = Flask(__name__)
app.config.from_object(config)

LISTEN_ALL = True

@app.route('/')
def index():
	return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit_code():
	s = ''

	s += request.values['probId'] + '<br>'
	s += request.values['lang'] + '<br>'
	s += '<pre><code>' + request.values['code'] + '</code></pre>'

	prob_id = request.values['probId']
	lang = request.values['lang']
	code = request.values['code']

	TEST_CASE = 4

	judger = judge.Judger()
	res = judger.judge(prob_id, judge.JUDGE_CPP, code, 3.0, 65536, TEST_CASE)

	res = [judge.result_type[x] for x in res]

	judger = None

	return ' '.join(res)

@app.route('/submission/<int:subId>')
def submission_page(sub_id):
	return 'test'

if __name__ == '__main__':
	if LISTEN_ALL:
		app.run(host='0.0.0.0')
	else:
		app.run()