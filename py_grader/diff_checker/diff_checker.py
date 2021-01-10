import os
import re
import subprocess
import sys

temp_filename = 'diff_temp_'

"""
This whole ssytem relies on you using the diffchecker.com cli tool which is a node package
It will also open a browser window if a browser is available
You need to sign in the first time you use the tool
"""


def get_diff_msg(str_1, str_2):
	msg = []
	if str_1 == str_2:
		msg.append('The outputs are identical:')
		msg.append(str_1)
	else:
		msg.append('The outputs differ.')
		msg.append('Expected:')
		msg.append(str_1)
		msg.append('Actual:')
		msg.append(str_2)
		msg.append(diff_strings(str_1, str_2))
	return '\n'.join(msg)


def diff_strings(str_1, str_2):
	filename_1 = temp_filename + '1.txt'
	filename_2 = temp_filename + '2.txt'
	with open(filename_1) as f:
		f.write(str_1)
	with open(filename_2) as f:
		f.write(str_2)
	result = diff_files(filename_1, filename_2)
	os.remove(filename_1)
	os.remove(filename_2)
	return result


diff_url_re = re.compile(r'Your diff is ready: (https://www\.diffchecker\.com/.*)')


def diff_files(file_1, file_2):
	result = subprocess.check_output(['npx', 'diffchecker', file_1, file_2], stderr=subprocess.STDOUT,
	                                 shell=sys.platform == 'win32').decode('utf-8')
	re_match = re.search(diff_url_re, result)
	if not re_match:
		raise RuntimeError(f'No diff url found in output: {result}')
	return re_match[1]
