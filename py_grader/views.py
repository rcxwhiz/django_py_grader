import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

import py_grader.config as cfg
from py_grader.forms import CreateAssignmentForm, SubmitAssignmentForm, ChooseAssignmentForm, SubmitPyFile, \
	ViewSubmissionForm, NetIDNameForm, CSVFileForm, AddTestCaseForm, NetIDForm
from py_grader.handler import process_assignment, process_submission, process_test_submission, add_net_id_db, \
	remove_net_id_db, clear_net_id_db, upload_net_id_csv_db, add_test_case_db, get_student_assignment_report
from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase, NetID
from py_grader.util import error_list_from_form

logger = logging.getLogger(__name__)


def index(request):
	logger.debug('Serving student index')
	context = {
	}
	return render(request, 'py_grader/student/index/index.html', context)


@login_required(redirect_field_name='/grader')
def grader_index(request):
	logger.debug('Serving grader index')
	context = {
	}
	return render(request, 'py_grader/grader/index/index.html', context)


def submit(request, success_message=None, failure_message=None):
	logger.debug('Serving submit menu')
	# form = ChooseAssignmentForm()
	context = {
		'assignments': Assignment.objects.order_by('close_time')
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/student/submit/index.html', context)


def submit_get(request):
	logger.debug('Serving submit menu get method')
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		logger.debug('Valid submit assignment menu form')
		get_object_or_404(Assignment, assignment_name=form.cleaned_data['assignment_name'])
		logger.debug(f'Found assignment: {form.cleaned_data["assignment_name"]}')
		return redirect(f'/submit/{form.cleaned_data["assignment_name"]}/')
	logger.debug(f'Invalid submit assignment menu form: {error_list_from_form(form)}')
	return submit(request, failure_message=error_list_from_form(form))


def submit_assignment(request, assignment_name, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('Serving submit assignment post method')
		form = SubmitAssignmentForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid submit assignment form')
			get_object_or_404(Assignment, assignment_name=assignment_name)
			logger.debug(f'Found assignment: {assignment_name}')
			try:
				logger.debug(
					f'Processing assignment submission - assignment: {assignment_name}, NetID: {form.cleaned_data["net_id"]}')
				submission_result_id = process_submission(form, assignment_name, request.META['REMOTE_ADDR'])
				return redirect(f'view_submission_result/{submission_result_id}')
			except Exception as e:
				logging.info(
					f'Error processing assignemnt submission - assignment: {assignment_name}, NetID: {form.cleaned_data["net_id"]}, e: {e}')
				return submit_assignment(request, assignment_name, failure_message=f'Internal Error: {e}')
		logger.debug(f'Invalid submit assignment form: {error_list_from_form(form)}')
		return submit_assignment(request, assignment_name, failure_message=error_list_from_form(form))

	logger.debug('Serving submit assignment')
	form = SubmitAssignmentForm()
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'form': form,
		'assignment': assignment,
		'upload_limit': cfg.upload_limit_mbytes,
		'support_email': cfg.bad_email
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/student/submit/submit_assignment.html', context)


def test_submit(request, success_message=None, failure_message=None):
	logger.debug('Serving test submit menu')
	form = ChooseAssignmentForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/test_submit.html', context)


def test_submit_get(request):
	logger.debug('Serving test submit menu get method')
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		logger.debug('Valid test submit assignment menu form')
		get_object_or_404(Assignment, assignment_name=form.assignment_name)
		logger.debug(f'Found assignment: {form.assignment_name}')
		return redirect(f'test_submit/{form.assignment_name}/')
	logger.debug(f'Invalid test submit assignment menu form: {error_list_from_form(form)}')
	return test_submit(request, failure_message=error_list_from_form(form))


# TODO this is going to redirectto a result which is not saved in the database
@login_required(redirect_field_name='/grader')
def test_submit_assignment(request, assignment_name, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('Serving test submit post method')
		form = SubmitPyFile(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid test submit assignment form')
			get_object_or_404(Assignment, assignment_name=assignment_name)
			logger.debug(f'Found assignment: {assignment_name}')
			try:
				logger.debug(f'Processing assignment test submission - assignment: {assignment_name}')
				process_test_submission(form, assignment_name)
				return test_submit_assignment(request, assignment_name,
				                              success_message='Successfully Submitted Test Assignment')
			except Exception as e:
				logging.info(
					f'Error processing assignemnt test submission - assignment: {assignment_name}, e: {str(e)}')
				return test_submit_assignment(request, assignment_name, failure_message=str(e))
		logger.debug(f'Invalid test submit assignment form: {error_list_from_form(form)}')
		return test_submit_assignment(request, assignment_name, failure_message=error_list_from_form(form))

	logger.debug('Serving test submit')
	form = SubmitPyFile()
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'form': form,
		'assignment': assignment
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/test_submit_assignment.html', context)


@login_required(redirect_field_name='/grader')
def view_results(request, success_message=None, failure_message=None):
	logger.debug('Serving view assignment results menu')
	form = ChooseAssignmentForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_assignment_results.html', context)


def view_results_get(request):
	logger.debug('Serving view assignment results menu get method')
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		logger.debug('Valid view assignment results menu form')
		get_object_or_404(Assignment, assigment_name=form.assignment_name)
		logger.debug(f'Found assignment: {form.assignment_name}')
		return redirect(f'view_assignment_results/{form.assignment_name}/')
	logger.debug(f'Invalid view assignment results menu form: {error_list_from_form(form)}')
	return view_results(request, failure_message=error_list_from_form(form))


# TODO
@login_required(redirect_field_name='/grader')
def view_assignment_results(request, assignment_name, success_message=None, failure_message=None):
	logger.debug('Serving view assignment results')
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	student_report_dict = get_student_assignment_report(assignment)
	context = {
		'assignment': assignment,
		'students': student_report_dict
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_assignment_results.html', context)


def view_any_submission_result(request, success_message=None, failure_message=None):
	logger.debug('Serving view submission result menu')
	form = ViewSubmissionForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/student/view_submission/index.html', context)


def view_any_submission_result_get(request):
	logger.debug('Serving view submission result menu get method')
	form = ViewSubmissionForm(request.GET)
	if form.is_valid():
		logger.debug('Valid view submission result menu form')
		get_object_or_404(SubmissionResult, pk=form.cleaned_data['submission_number'])
		logger.debug(f'Found submission result: {form.cleaned_data["submission_number"]}')
		return redirect(f'view_submission_result/{form.cleaned_data["submission_number"]}/')
	logger.debug(f'Invalid view submission result menu form: {error_list_from_form(form)}')
	return view_any_submission_result(request, failure_message=error_list_from_form(form))


def view_submission_result(request, submission_id, success_message=None, failure_message=None):
	logger.debug('Serving view submission result')
	submission_result = get_object_or_404(SubmissionResult, submission=submission_id)
	logger.debug(f'Found submission result: {submission_id}')
	test_cases = TestCase.objects.order_by('test_case_number').filter(
		assignment=submission_result.submission.assignment.pk)
	logger.debug(f'Found {len(test_cases)} test cases to show with the submission result')
	submission_test_cases = [
		SubmissionCaseResult.objects.get(submission=submission_result.submission.pk, test_case=case.pk) for case in
		test_cases]
	context = {
		'submission_result': submission_result,
		'submission': submission_result.submission,
		'test_cases': test_cases,
		'submission_test_cases': submission_test_cases
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_submission_result.html', context)


@login_required(redirect_field_name='/grader')
def create_assignment(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('Serving create assignment post method')
		form = CreateAssignmentForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid create assignment form')
			try:
				logger.debug(f'Creating assignment: {form.cleaned_data["assignment_name"]}')
				process_assignment(form)
				return create_assignment(request, success_message='Successfully Created Assignment')
			except Exception as e:
				logging.info(f'Error creating assignment {form.cleaned_data["assignment_name"]} - e: {str(e)}')
				return create_assignment(request, failure_message=str(e))
		logger.debug(f'Invalid create assignment form: {error_list_from_form(form)}')
		return create_assignment(request, failure_message=error_list_from_form(form))

	logger.debug('Serving create assignment')
	form = CreateAssignmentForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/create_assignment.html', context)


@login_required(redirect_field_name='/grader')
def add_any_test_case(request, success_message=None, failure_message=None):
	logger.debug('Serving add any test case')
	form = ChooseAssignmentForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/add_any_test_case.html', context)


def add_any_test_case_get(request):
	logger.debug('Serving add any test case get')
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		logger.debug('Valid add any test case form')
		assignment_name = form.cleaned_data['assignment_name']
		get_object_or_404(Assignment, assignment_name=assignment_name)
		logger.debug(f'Found assignment: {assignment_name}')
		return redirect(f'/grader/add_test_case/{assignment_name}')
	logger.debug(f'Invalid add any test case form: {error_list_from_form(form)}')
	return add_any_test_case(request, failure_message=error_list_from_form(form))


@login_required(redirect_field_name='/grader')
def add_test_case(request, assignment_name, success_message=None, failure_message=None):
	logger.debug(f'Add test case checking for assignment: {assignment_name}')
	get_object_or_404(Assignment, assignment_name=assignment_name)
	if request.method == 'POST':
		logger.debug('Serving add test case post method')
		form = AddTestCaseForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid add test case form')
			try:
				logger.debug(f'Adding test case to {assignment_name}')
				add_test_case_db(form, assignment_name)
				return add_test_case(request, assignment_name, success_message='Successfully Added Test Case')
			except Exception as e:
				logger.info(f'Error adding test case to {assignment_name}: {str(e)}')
				return add_test_case(request, assignment_name, failure_message=str(e))
		logger.debug(f'Invalid add test case form: {error_list_from_form(form)}')
		return add_test_case(request, assignment_name, failure_message=error_list_from_form(form))

	logger.debug('Serving add test case')
	form = AddTestCaseForm()
	context = {
		'form': form,
		'assignment_name': assignment_name
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/add_test_case.html', context)


@login_required(redirect_field_name='/grader')
def manage_net_ids(request, success_message=None, failure_message=None):
	logger.debug('Serving manage net ids')
	context = {
		'net_ids': NetID.objects.order_by('net_id')
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/manage_net_ids.html', context)


@login_required(redirect_field_name='/grader')
def add_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('Serving add net id post method')
		form = NetIDNameForm(request.POST)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid add net id form')
			try:
				logger.debug(f'Adding NetID: {form.net_id}')
				add_net_id_db(form)
				return add_net_id(request, success_message='Successfully Added NetID')
			except Exception as e:
				logger.info(f'Error adding NetID {form.net_id}: {str(e)}')
				return add_net_id(request, failure_message=str(e))
		logger.debug(f'Invalid add net id form: {error_list_from_form(form)}')
		return add_net_id(request, failure_message=error_list_from_form(form))

	logger.debug('serving add net id')
	form = NetIDNameForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/add_net_id.html', context)


@login_required(redirect_field_name='/grader')
def remove_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('serving remove net id post method')
		form = NetIDForm(request.POST)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid remove net id form')
			try:
				logger.debug(f'Removing NetID: {form.net_id}')
				remove_net_id_db(form)
				return remove_net_id(request, success_message='Successfully Removed NetID')
			except Exception as e:
				logger.info(f'Error removing NetID {form.net_id}: {str(e)}')
				return remove_net_id(request, failure_message=str(e))
		logger.debug(f'Invalid remove net id form: {error_list_from_form(form)}')
		return remove_net_id(request, failure_message=error_list_from_form(form))

	logger.debug('Serving remove net id')
	form = NetIDForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/remove_net_id.html', context)


@login_required(redirect_field_name='/grader')
def upload_net_id_csv(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('Serving upload net id csv post method')
		form = CSVFileForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			logger.debug('Valid upload net id csv form')
			try:
				logger.debug(f'Uploading NetID CSV file: {form.cleaned_data.get("csv_file").name}')
				num_uploaded = upload_net_id_csv_db(form)
				return upload_net_id_csv(request, success_message=f'Successfully Uploaded {num_uploaded} NetIDs')
			except Exception as e:
				logger.info(f'Error uploading NetID CSV file {form.cleaned_data.get("csv_file").name}: {str(e)}')
				return upload_net_id_csv(request, failure_message=str(e))
		logger.debug(f'Invalid upload net id csv form: {error_list_from_form(form)}')
		return upload_net_id_csv(request, failure_message=error_list_from_form(form))

	logger.debug('Serving upload net id csv post method')
	form = CSVFileForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/upload_net_id_csv.html', context)


@login_required(redirect_field_name='/grader')
def clear_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		logger.debug('serving clear net ids post method')
		request.method = 'GET'
		try:
			logger.debug('Clearing NetIDs')
			clear_net_id_db()
			return clear_net_id(request, success_message='Successfully Cleared NetIDs')
		except Exception as e:
			logger.debug(f'Error clearing NetIDs: {str(e)}')
			return clear_net_id(request, failure_message=str(e))

	logger.debug('Serving clear net ids')
	context = {
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/remove_net_id.html', context)


@login_required(redirect_field_name='/grader')
def assignments(request):
	logger.debug('Serving View Assignments')
	context = {
		'assignments': Assignment.objects.order_by('close_time'),
		'number_students': NetID.objects.all().count()
	}
	return render(request, 'py_grader/grader/assignment/index.html', context)
