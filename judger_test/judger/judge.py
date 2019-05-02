import subprocess as sp
import os, sys, shutil
import json
from pathlib import Path

from utils import dump

JUDGE_C   = 0
JUDGE_CPP = 1

'''
1 AC
2 RE
3 CE
4 TLE
5 MLE
6 WA
7 PE
8 OLE
9 OTHER
10 SYS_ERR
11 Restricted Function
'''

cur_path = os.path.join(os.getcwd(), 'judger')

compile_inc_path = os.path.join(cur_path, 'compile')
box_path = lambda box_id, *p: os.path.join('/var/local/lib/isolate/', str(box_id), 'box', *p)
meta = lambda box_id, *p: os.path.join(cur_path, 'meta', str(box_id), *p)
res_path = lambda box_id, *p: os.path.join(cur_path, 'res', str(box_id), *p)
data_path = lambda *p: os.path.join(cur_path, 'testdata', *p)

def get_isolate_arg(box_id, time, wall_time, wall_mem, fsize, proc_num, bind_dir
	, meta_path, stdin=None, stdout=None, stderr=None, redir=False):
	arg_list = [ '--box-id={}'.format(box_id)
				,'--silent'
				, '--time={:.2f}'.format(time)
				, '--wall-time={:.2f}'.format(wall_time)
				, '--fsize={:d}'.format(fsize)
				, '--processes={:d}'.format(proc_num)
				]

	# Append memory limit
	# if wall_mem:
	# 	arg_list.append('--wall-mem={:d}'.format(wall_mem))
	# TODO(roy4801): This is a workaround
	if wall_mem:
		arg_list.append('--mem={:d}'.format(wall_mem))

	# Append the dir
	if isinstance(bind_dir, str):
		arg_list.append('--dir={}'.format(bind_dir))
	elif isinstance(bind_dir, list):
		for i in bind_dir:
			arg_list.append('--dir={}'.format(i))

	arg_list.append('-e')
	arg_list.append('--meta={}'.format(meta_path))
	
	if stdin:
		arg_list.append('--stdin={}'.format(stdin))
	if stdout:
		arg_list.append('--stdout={}'.format(stdout))
	if stderr:
		arg_list.append('--stderr={}'.format(stderr))
	if redir:
		arg_list.append('--stderr-to-stdout')
		
	return arg_list


def get_compile_arg_cpp(box_id, lang_spec='c++11'
	, code_file='code.cpp', exe_path='submit', inc_path=compile_inc_path):
	arg_list = get_isolate_arg(box_id, 60.0, 60.0, None, 65536, 64, cur_path
		, meta(box_id, 'compile_meta'), None, 'compile_out', None, True)
	arg_list.append('--run')
	arg_list.append('--')
	arg_list += '/usr/bin/env g++ {} -I{} -Wall -Wshadow -Wno-unused-result -static -O2 -std={} -o {}'.format(code_file, inc_path, lang_spec, exe_path).split()
	
	return arg_list

def get_run_arg(box_id, cur_case, time_lim, mem_lim, in_file, out_file):
	arg_list = get_isolate_arg(box_id, time_lim, time_lim*1.5, mem_lim, 65536, 64, cur_path
		, meta(box_id, 'run_meta_{}'.format(cur_case)), in_file, out_file, None, True)
	arg_list.append('--run')
	arg_list.append('--')
	arg_list.append('./submit')

	return arg_list

def get_checkans_arg(box_id, cur_case, in_file, out_file, ans_file):
	arg_list = get_isolate_arg(box_id, 60.0, 60.0, None, 65536, 64, cur_path
		, meta(box_id, 'checkans_meta_{}'.format(cur_case)), '/dev/null', '/dev/null', '/dev/null', False)
	arg_list.append('--run')
	arg_list.append('--')
	arg_list += './checkans {} {} {}'.format(in_file, out_file, ans_file).split()

	return arg_list

def runCmd(cmd, *args, **kwargs):
	if isinstance(cmd, str):
		cmd = cmd.split()
	p = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, *args, **kwargs)
	return p

def move(fr, to):
	return not runCmd('mv {} {}'.format(fr, to)).returncode

def copy(fr, to):
	# print('RUN cp {} {}'.format(fr, to))
	return not runCmd('cp {} {}'.format(fr, to)).returncode

def mkdir(path):
	return not runCmd('mkdir -p {}'.format(path)).returncode

def rmrf(path):
	return not runCmd('rm -rf {}'.format(path)).returncode

MAX_ISO = 4096
class Isolate:
	STATE = [False] * MAX_ISO
	NOW_BOX = 0
	USING = []
	UNUSE = [i for i in range(MAX_ISO)]

	@staticmethod
	def get_box_id():
		free_id = Isolate.UNUSE.pop(0)
		Isolate.USING.append(free_id)
		Isolate.NOW_BOX += 1
		Isolate.STATE[free_id] = True
		return free_id

	@staticmethod
	def free_box(box_id):
		Isolate.UNUSE.append(box_id)
		Isolate.USING.remove(box_id)
		Isolate.NOW_BOX -= 1
		Isolate.STATE[box_id] = False

	@staticmethod
	def is_box_id_free(i):
		return not Isolate.STATE[i]

	def __init__(self):
		# Get the box id
		self.box_id = Isolate.get_box_id()

		ret = runCmd('isolate --box-id={} --init'.format(self.box_id))

		# Failed
		if ret == 127:
			print('isolate box {} failed to init'.format(self.box_id))
			sys.exit(-1)
		else:
			print('isolate box {} inited'.format(self.box_id))
			rmrf(meta(self.box_id))
			rmrf(res_path(self.box_id))

			mkdir(meta(self.box_id))
			mkdir(res_path(self.box_id))

	def release_box(self):
		box_id = self.box_id
		# isolate --box-id={self.box_id} --cleanup 2>/dev/null >/dev/null
		ret = runCmd('isolate --box-id={} --cleanup'.format(box_id)).returncode
		# Failed
		if ret == 127:
			print('isolate box {} failed to cleanup'.format(box_id))
			sys.exit(-1)
		else:
			print('isolate box {} cleanup'.format(box_id))

		# Free the box id
		Isolate.free_box(box_id)

	def get_cur_box_id(self):
		return self.box_id

def meta_to_json(path):
	data = None

	if not Path(path).exists():
		return '{}'

	with open(path, 'r') as f:
		data = f.readlines()

	# print(data)

	flag = False
	res = '{'
	for i in data:
		if flag:
			res += ','
		i = i.split(':')
		if '"' in i[1]:
			i[1] = i[1].replace('"', r'\"')
		if 'status' in i or 'message' in i:
			i[1] = '"{}"'.format(i[1].strip('\n'))
		res += '"{}":{}'.format(i[0], i[1].strip('\n'))
		flag = True
	res += '}'

	return res

RES_AC      = 1
RES_RE      = 2
RES_CE      = 3
RES_TLE     = 4
RES_MLE     = 5
RES_WA      = 6
RES_PE      = 7
RES_OLE     = 8
RES_OTHER   = 9
RES_SYS_ERR = 10
RES_RF      = 11

result_type = { 1 : 'AC' #
			   ,2 : 'RE'
			   ,3 : 'CE' #
			   ,4 : 'TLE'#
			   ,5 : 'MLE'
			   ,6 : 'WA'
			   ,7 : 'PE'
			   ,8 : 'OLE'
			   ,9 : 'OTHER'
			   ,10: 'SYS_ERR'
			   ,11: 'RF' }

META_COMPILE  = 0
META_RUN      = 1
META_CHECKANS = 2
class Judger:
	def __init__(self):
		self.box = Isolate()
		self.meta = {}

	def end(self):
		self.box.release_box()

	def parse_meta(self, meta_type, i=0):
		box_id = self.box.get_cur_box_id()

		if meta_type == META_COMPILE:
			self.meta['compile'] = json.loads(meta_to_json(meta(box_id, 'compile_meta')))
		elif meta_type == META_RUN:
			self.meta['run_{}'.format(i)] = json.loads(meta_to_json(meta(box_id, 'run_meta_{}'.format(i))))
		elif meta_type == META_CHECKANS:
			# print('Add dict {}'.format('checkans_{}'.format(i)))
			self.meta['checkans_{}'.format(i)] = json.loads(meta_to_json(meta(box_id, 'checkans_meta_{}'.format(i))))

	def debug_dump(self, i):
		meta = self.meta
		print('=== Case {} ==='.format(i))

		self.parse_meta(META_COMPILE)
		print('=== compile_meta ===')
		dump(meta['compile'])

		self.parse_meta(META_RUN, i)
		print('=== run_meta ===')
		dump(meta['run_{}'.format(i)])

		self.parse_meta(META_CHECKANS, i)
		print('=== checkans_meta ===')
		dump(meta['checkans_{}'.format(i)])
		print('==============\n')

	def judge(self, prob_id, lang, code, time_lim, mem_lim, test_case):
		box_id = self.box.get_cur_box_id()

		self.compile(code, lang)

		self.parse_meta(META_COMPILE)
		if self.meta['compile']['exitcode']:
			self.end()
			return [RES_CE] * test_case

		# prepare the testdata for copying into the box
		for i in range(test_case):
			copy(data_path('{}_{}.in'.format(prob_id, i)), res_path(box_id, 'in_{}'.format(i)))
			copy(data_path('{}_{}.ans'.format(prob_id, i)), res_path(box_id, 'ans_{}'.format(i)))

		res = []
		for i in range(test_case):
			run_name = 'run_{}'.format(i)
			checkans_name = 'checkans_{}'.format(i)

			res.append(-1)

			# Run the program for i-th testcase
			self.run(i, time_lim, mem_lim, 'in_'+str(i), 'out_'+str(i))
			self.parse_meta(META_RUN, i)
			run_meta = self.meta[run_name]
			if ('status' in run_meta and run_meta['status'] == 'TO') or run_meta['time'] > time_lim:
				res[i] = RES_TLE
				continue
			elif ('status' in run_meta and run_meta['status'] == 'ML') or run_meta['max-rss'] > mem_lim:
				res[i] = RES_MLE
				continue
			elif ('status' in run_meta and run_meta['status'] == 'SG') and ('exitsig' in run_meta and run_meta['exitsig'] == 11): # RE
				res[i] = RES_RE
				continue

			# check ans
			self.check_ans(i, 'in_'+str(i), 'out_'+str(i), 'ans_'+str(i))
			self.parse_meta(META_CHECKANS, i)
			if self.meta[checkans_name]['exitcode'] == 1:
				res[i] = RES_AC
			else:
				res[i] = RES_WA
		self.end()
		return res

	# private
	def compile(self, code, lang):
		box = self.box
		i = box.get_cur_box_id()
		# TODO(roy4801): Support for C
		if lang == JUDGE_C:
			print("Unsupported language")
			sys.exit(-1)
		# Write to file `code.cpp` inside the box
		with open(box_path(i, 'code.cpp'), 'w') as f:
			f.write(code)

		# Compile the program
		cmd = ['isolate'] + get_compile_arg_cpp(i)
		# dump(cmd)
		runCmd(cmd)

		# Copy the compile msg
		copy(box_path(i, 'compile_out'), res_path(i, 'compile_out'))

	def run(self, cur_case, time_lim, mem_lim, inp, outp,):
		box = self.box
		i = box.get_cur_box_id()

		# Copy the in data
		copy('{}'.format(res_path(i, inp)), '{}/{}'.format(box_path(i), inp))
		
		# Run the program
		cmd = ['isolate'] + get_run_arg(i, cur_case, time_lim, mem_lim, inp, outp)
		runCmd(cmd)
		
		# Copy the out data
		copy('{}/{}'.format(box_path(i), outp), '{}'.format(res_path(i, outp)))

	def check_ans(self, cur_case, prog_in, prog_out, ac_out):
		box = self.box
		i = box.get_cur_box_id()

		# Copy checkans
		copy(os.path.join(compile_inc_path, 'checkans'), os.path.join(box_path(i), 'checkans'))
		# runCmd('cp compile/checkans {}/checkans'.format(box_path(i)))
		
		copy(res_path(i, ac_out), os.path.join(box_path(i), ac_out))
		# runCmd('cp {0} {1}/{2}'.format(res_path(i, ac_out), box_path(i), ac_out))

		cmd = ['isolate'] + get_checkans_arg(i, cur_case, prog_in, prog_out, ac_out)
		runCmd(cmd)