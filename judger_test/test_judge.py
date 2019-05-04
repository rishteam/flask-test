import sys
sys.path.append('./judger/')

from judge import *
from utils import dump
import json

code = ''
with open('../testProb/1.cpp', 'r') as f:
	code = ''.join(f.readlines())


# tmp = []
# for _ in range(10):
# 	tmp.append(Judger())
a = Judger()

CASE = 4

res = a.judge(1, JUDGE_CPP, code, 3.0, 65536, CASE)

x = [result_type[i] for i in res]
print(x)

for i in range(CASE):
	a.debug_dump(i)

