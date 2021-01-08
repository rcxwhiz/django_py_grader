import logging
import os
from datetime import datetime

import pandas as pd
from django.db import IntegrityError

from py_grader.docker_tools import CodeRunner
from py_grader.models import Assignment, NumberSubmissions, NetID, TestCase, SubmissionCaseResult, \
	Submission, SubmissionResult, TestCaseFile, GradingMethod

logger = logging.getLogger(__name__)


def process_assignment(form):
	assignment = Assignment()
	data = form.cleaned_data
	logger.info(f'Creating new assignment: {data.get("assignment_name")}')
	assignment.assignment_name = data.get('assignment_name')
	logger.debug(f'Processing Python key file: {data.get("key_source_code").name}')
	in_memory_code = data.get('key_source_code')
	code_text = ''
	for line in in_memory_code:
		code_text += line.decode()
	assignment.key_source_code = code_text
	logger.debug('Setting other assignment fields')
	assignment.open_time = data.get('open_time')
	assignment.close_time = data.get('close_time')
	assignment.total_submissions = 0
	assignment.number_students_submited = 0
	assignment.number_submissions_allowed = data.get('number_submissions')
	assignment.number_test_cases = 0
	assignment.grading_method = data.get('grading_method')
	assignment.allowed_packages = data.get('allowed_packages')
	logger.debug(f'Saving assignment: {data.get("assignment_name")}')
	assignment.save()

	logger.debug('Initializing student submissions to 0')
	for net_id in NetID.objects.all():
		num_submissions = NumberSubmissions()
		num_submissions.net_id = net_id
		num_submissions.assignment = assignment
		num_submissions.number_submissions = 0
		num_submissions.save()


# TODO
def process_test_submission(form, assignment_name):
	logger.info('Process test submission unimplemented')


class SubmissionException(Exception):
	def __init__(self, msg):
		super(msg)


def calculate_grade(submission_case_results, grading_method):
	if grading_method == 'ALL_OR_NOTHING':
		logger.debug('Calculating an all or nothing grade')
		for result in submission_case_results:
			if not result.correct:
				return 0
		return 100
	elif grading_method == 'FRACTION':
		correct = 0
		for result in submission_case_results:
			if result.correct:
				correct += 1
		result = round(correct / len(submission_case_results) * 100)
		logger.debug(f'Calculated a fractional grade {correct}/{len(submission_case_results)} ({result})')
		return result
	elif grading_method == 'FRACTION_SEQUENTIAL':
		correct = 0
		for result in submission_case_results:
			if result.correct:
				correct += 1
			else:
				break
		result = round(correct / len(submission_case_results) * 100)
		logger.debug(f'Calculated a sequential fractional grade {correct}/{len(submission_case_results)} ({result})')
		return result
	elif grading_method == 'COMPLETION':
		logger.debug('Calculating a completion grade')
		return 100
	else:
		logger.warning(f'Got an unrecognized grading method: {grading_method}')
		raise RuntimeError(f'Unrecognized Grading Method: {grading_method}')


def process_submission(form, assignment_name, ip_address):
	logger.info(f'Processing a submission for {assignment_name} from {ip_address}')
	data = form.cleaned_data

	# create and save submission
	submission = Submission()
	net_id = NetID.objects.get(net_id=data.get('net_id'))
	logger.debug(f'Got NetID: {data.get("net_id")}')
	submission.net_id = net_id
	assignment = Assignment.objects.get(assignment_name=assignment_name)
	submission.assignment = assignment
	logger.debug(f'Get assignment: {assignment_name}')
	logger.debug(f'Processing submission code: {data.get("student_source_code").name}')
	in_memory_code = data.get('student_source_code')
	code_text = ''
	for line in in_memory_code:
		code_text += line.decode()
	submission.submission_source_code = code_text
	logger.debug('Populating other submission fields')
	submission.submission_time = datetime.now()
	num_submissions = NumberSubmissions.objects.filter(net_id=net_id, assignment=assignment)
	submission.submission_number = num_submissions.number_submissions + 1
	submission.ip_address = ip_address
	logger.debug('Saving submission')
	submission.save()

	# check number submissions
	logger.debug(
		f'Checking for valid number of submissions ({submission.submission_number}/{assignment.number_submissions_allowed})')
	if not submission.submission_number <= assignment.number_submissions_allowed:
		logger.debug('Number allowed submissions exceded')
		raise SubmissionException(f'{submission.submission_number}/{assignment.number_submissions_allowed} Used')
	num_submissions.number_submissions += 1
	logger.debug('Updating number of submissions')
	num_submissions.save()

	# find test cases for that assignment
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=assignment)
	logger.debug(f'Found {len(test_cases)} test cases for {assignment_name}')

	temp_filename = f'{net_id.net_id}_temp.py'
	logger.debug(f'Using temp code file: {temp_filename}')

	# create code runner
	logger.debug('Making code runner')
	code_runner = CodeRunner()
	code_runner.set_filename(temp_filename)
	packages = assignment.allowed_packages.split()
	logger.debug('Adding code runner packages')
	for package in packages:
		code_runner.add_package(package)

	logger.debug('Writing student code to temp file')
	with open(temp_filename, 'w') as temp_f:
		temp_f.write(submission.submission_source_code)

	# run the code against each of those and make a list of results
	submission_case_results = []
	for test_case in test_cases:
		logger.debug(f'Running test case {test_case.test_case_number}')

		# copy the files for the test case
		logger.debug('Copying over appropiate files')
		test_case_files = TestCaseFile.objects.filter(test_case=test_case)
		code_runner.clear_files()
		for test_case_file in test_case_files:
			with open(f'temp_files/{test_case_file.name}', 'w') as f:
				db_f = test_case_file.test_case_file.open('r')
				f.write(db_f.read())
				code_runner.add_file(f'temp_files/{test_case_file.name}', test_case_file.name)

		logger.debug('Creating a submission case result')
		submission_case_result = SubmissionCaseResult()
		submission_case_result.submission = submission
		submission_case_result.test_case = test_case
		submission_case_result.test_case_number = test_case.test_case_number
		submission_case_result.expected_output = test_case.test_case_output

		logger.debug('Running code and saving output')
		submission_case_result.submission_output = code_runner.run()
		submission_case_result.correct = (
					submission_case_result.expected_output == submission_case_result.submission_output)

		logger.debug('Saving submission case result')
		submission_case_result.save()
		submission_case_results.append(submission_case_result)

		logger.debug('Cleaning test case files')
		for test_case_file in test_case_files:
			os.remove(f'temp_files/{test_case_file.name}')

	# calculate a total grade
	logger.debug('Calculating total grade')
	grade = calculate_grade(submission_case_results, assignment.grading_method.grading_method)

	# put in a submission result
	logger.debug('Creating submission result')
	submission_result = SubmissionResult()
	submission_result.submission = submission
	submission_result.submission_grade = grade
	logger.debug('Saving submission result')
	submission_result.save()

	logger.debug('Removing temp code file')
	os.remove(temp_filename)

	return submission_result.pk


def add_net_id_db(form):
	logger.info('Creating NetID')
	net_id = NetID()
	data = form.cleaned_data
	logger.debug(f'Using NetID: {data.get("net_id")}')
	net_id.net_id = data.get('net_id')
	logger.debug(f'Using name: {data.get("name")}')
	net_id.name = data.get('name')
	logger.debug(f'Using first name: {data.get("first_name")}')
	net_id.first_name = data.get('first_name')
	logger.debug(f'Using last name: {data.get("last_name")}')
	net_id.last_name = data.get('last_name')

	logger.debug('Saving NetID')
	net_id.save()

	logger.debug('Initializing student submissions to 0')
	assignments = Assignment.objects.all()
	for assignment in assignments:
		num_submissions = NumberSubmissions()
		num_submissions.net_id = net_id
		num_submissions.assignment = assignment
		num_submissions.number_submissions = 0
		num_submissions.save()


def remove_net_id_db(form):
	logger.info(f'Removing NetID: {form.cleaned_data.get("net_id")}')
	net_id = NetID.objects.get(net_id=form.cleaned_data.get('net_id'))
	net_id.delete()


byu_csv_header = 'Name,NetID,Email,Major,Last View,Total Views,'


def upload_net_id_csv_db(form):
	in_memory_csv = form.cleaned_data.get('csv_file')
	logger.info(f'Getting NetIDs from: {in_memory_csv.name}')

	csv_type = 'OTHER'
	with open(in_memory_csv) as f:
		if f.read().startswith(byu_csv_header):
			csv_type = 'BYU'

	logger.debug(f'Detected csv type: {csv_type}')

	if csv_type == 'BYU':
		csv = pd.read_csv(in_memory_csv,
		                  names=['Name', 'NetID', 'Email', 'Major', 'Last View', 'Total Views', 'Something',
		                         'Something else'])
		csv = csv.iloc[1:]
	else:
		csv = pd.read_csv(in_memory_csv)

	num_saved = 0

	logger.debug('Saving rows')
	# TODO this probably doesn't work
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
	logger.info('Clearing NetIDs from database')
	NetID.objects.all().delete()


def add_test_case_db(form, assignment_name):
	data = form.cleaned_data
	logger.info(f'Adding test case for assignment: {assignment_name}')
	test_case = TestCase()
	assignment = Assignment.objects.get(assignment_name=assignment_name)
	test_case.assignment = assignment
	assignment.number_test_cases += 1
	test_case.test_case_number = assignment.number_test_cases
	test_case.test_case_input = data.get('test_case_input')
	logger.debug(f'Populated fields for test case: {test_case.test_case_number} and saving')

	test_case.save()

	logger.debug('Creating test file entries for test case')
	for file in form.files.getlist('test_case_files'):
		t_file = TestCaseFile()
		t_file.test_case = test_case
		t_file.test_case_file = file
		t_file.save()

	logger.debug('Assignment')
	assignment.save()


grading_methods = ['ALL OR NOTHING', 'FRACTION', 'FRACTION SEQUENTIAL', 'COMPLETION']


def add_grading_methods_to_db():
	for grading_method in grading_methods:
		method = GradingMethod()
		method.grading_method = grading_method
		try:
			method.save()
		except IntegrityError:
			pass


def get_student_assignment_report(assignment):
	students = [
		{'net_id': net_id.net_id, 'name': net_id.name, 'first_name': net_id.first_name, 'last_name': net_id.last_name}
		for net_id in NetID.objects.order_by('net_id')]
	for student in students:
		net_id = NetID.objects.get(net_id=student['net_id'])
		num_submissions = NumberSubmissions.objects.get(net_id=student['net_id'], assignment=assignment)
		student['num_submissions'] = num_submissions
		if num_submissions == 0:
			student['grade'] = 0
		else:
			last_submission = Submission.objects.get(assignment_name=assignment, net_id=net_id,
			                                         submission_number=num_submissions)
			last_submission_result = SubmissionResult.objects.get(submission=last_submission)
			student['grade'] = last_submission_result.submission_grade

	return students
