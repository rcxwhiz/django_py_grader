import os
from datetime import datetime

import pandas as pd

from py_grader.docker_tools import CodeRunner
from py_grader.models import Assignment, GradingMethod, NumberSubmissions, NetID, TestCase, SubmissionCaseResult, \
	Submission, SubmissionResult, TestCaseFile


def process_assignment(form):
	assignment = Assignment()
	data = form.cleaned_data
	assignment.assignment_name = data.get('assignment_name')
	in_memory_code = data.get('key_source_code')
	code_text = ''
	for line in in_memory_code:
		code_text += line.decode()
	assignment.key_source_code = code_text
	assignment.open_time = data.get('open_time')
	assignment.close_time = data.get('close_time')
	assignment.total_submissions = 0
	assignment.number_students_submited = 0
	assignment.number_submissions_allowed = data.get('number_submissions')
	assignment.number_test_cases = 0
	assignment.grading_method = GradingMethod.objects.get(pk=data.get('grading_method'))
	assignment.allowed_packages = data.get('allowed_packages')
	assignment.save()


# TODO
def process_test_submission(form, assignment_name):
	pass


class SubmissionException(Exception):
	def __init__(self, msg):
		super(msg)


def calculate_grade(submission_case_results, grading_method):
	if grading_method == 'ALL_OR_NOTHING':
		for result in submission_case_results:
			if not result.correct:
				return 0
		return 100
	elif grading_method == 'FRACTION':
		correct = 0
		for result in submission_case_results:
			if result.correct:
				correct += 1
		return round(correct / len(submission_case_results) * 100)
	elif grading_method == 'FRACTION_SEQUENTIAL':
		correct = 0
		for result in submission_case_results:
			if result.correct:
				correct += 1
			else:
				return round(correct / len(submission_case_results) * 100)
		return round(correct / len(submission_case_results) * 100)
	elif grading_method == 'COMPLETION':
		return 100
	else:
		raise RuntimeError(f'Unrecognized Grading Method: {grading_method}')


def process_submission(form, assignment_name, ip_address):
	data = form.cleaned_data

	# create and save submission
	submission = Submission()
	net_id = NetID.objects.get(net_id=data.get('net_id'))
	submission.net_id = net_id
	assignment = Assignment.objects.get(assignment_name=assignment_name)
	submission.assignment = assignment
	in_memory_code = data.get('student_source_code')
	code_text = ''
	for line in in_memory_code:
		code_text += line.decode()
	submission.submission_source_code = code_text
	submission.submission_time = datetime.now()
	num_submissions = NumberSubmissions.objects.filter(net_id=net_id, assignment=assignment)
	submission.submission_number = num_submissions.number_submissions + 1
	submission.ip_address = ip_address
	submission.save()

	# check number submissions
	if not submission.submission_number <= assignment.number_submissions_allowed:
		raise SubmissionException(f'{submission.submission_number}/{assignment.number_submissions_allowed} Used')
	num_submissions.number_submissions += 1
	num_submissions.save()

	# find test cases for that assignment
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=assignment)

	temp_filename = f'{net_id.net_id}_temp.py'

	# create code runner
	code_runner = CodeRunner()
	code_runner.set_filename(temp_filename)
	packages = assignment.allowed_packages.split()
	for package in packages:
		code_runner.add_package(package)

	with open(temp_filename, 'w') as temp_f:
		temp_f.write(submission.submission_source_code)

	# run the code against each of those and make a list of results
	submission_case_results = []
	for test_case in test_cases:

		# copy the files for the test case
		test_case_files = TestCaseFile.objects.filter(test_case=test_case)
		code_runner.clear_files()
		for test_case_file in test_case_files:
			with open(f'temp_files/{test_case_file.name}', 'w') as f:
				db_f = test_case_file.test_case_file.open('r')
				f.write(db_f.read())
				code_runner.add_file(f'temp_files/{test_case_file.name}', test_case_file.name)

		submission_case_result = SubmissionCaseResult()
		submission_case_result.submission = submission
		submission_case_result.test_case = test_case
		submission_case_result.test_case_number = test_case.test_case_number
		submission_case_result.expected_output = test_case.test_case_output

		submission_case_result.submission_output = code_runner.run()
		submission_case_result.correct = (submission_case_result.expected_output == submission_case_result.submission_output)

		submission_case_result.save()
		submission_case_results.append(submission_case_result)

		for test_case_file in test_case_files:
			os.remove(f'temp_files/{test_case_file.name}')

	# calculate a total grade
	grade = calculate_grade(submission_case_results, assignment.grading_method.grading_method)

	# put in a submission result
	submission_result = SubmissionResult()
	submission_result.submission = submission
	submission_result.submission_grade = grade
	submission_result.save()

	os.remove(temp_filename)

	return submission_result.pk


def add_net_id_db(form):
	net_id = NetID()
	data = form.cleaned_data
	net_id.net_id = data.get('net_id')
	net_id.name = data.get('name')
	net_id.first_name = data.get('first_name')
	net_id.last_name = data.get('last_name')

	net_id.save()


def remove_net_id_db(form):
	net_id = NetID.objects.get(net_id=form.cleaned_data.get('net_id'))
	net_id.delete()


byu_csv_header = 'Name,NetID,Email,Major,Last View,Total Views,'


def upload_net_id_csv_db(form):
	in_memory_csv = form.cleaned_data.get('csv_file')

	csv_type = 'OTHER'
	with open(in_memory_csv) as f:
		if f.read().startswith(byu_csv_header):
			csv_type = 'BYU'

	if csv_type == 'BYU':
		csv = pd.read_csv(in_memory_csv,
		                  names=['Name', 'NetID', 'Email', 'Major', 'Last View', 'Total Views', 'Something',
		                         'Something else'])
		csv = csv.iloc[1:]
	else:
		csv = pd.read_csv(in_memory_csv)

	num_saved = 0

	for i, row in csv.iterrows():
		try:
			nid = NetID()
			nid.net_id = row['NetID']
			nid.name = row['Name']
			nid.first_name = row['First Name']
			nid.last_name = row['Last Name']
			nid.save()
			num_saved += 1
		except Exception as e:
			print(f'Failed to Add Row {i}: {str(e)}')

	return num_saved


def clear_net_id_db():
	NetID.objects.all().delete()


def add_test_case_db(form):
	pass
