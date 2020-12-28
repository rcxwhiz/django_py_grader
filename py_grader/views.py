from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from py_grader.handler import process_assignment, process_submission, process_test_submission, add_net_id_db, \
	remove_net_id_db, clear_net_id_db, upload_net_id_csv_db
from py_grader.forms import CreateAssignmentForm, SubmitAssignmentForm, ChooseAssignmentForm, SubmitPyFile, \
	ViewSubmissionForm, NetIDForm, CSVFileForm, AddTestCaseForm
from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase, GradingMethod, Submission
from py_grader.util import error_list_from_form


# TODO I should add back path variables for the methods that need them


def index(request):
	context = {
	}
	return render(request, 'py_grader/index.html', context)


def submit(request):
	if request.method == 'GET':
		form = ChooseAssignmentForm(request.GET)
		if form.is_valid():
			get_object_or_404(Assignment, assignment_name=form.assignment_name)
			return redirect(f'submit/{form.assignment_name}/')
		return failure(request, 'submit/', error_list_from_form(form))

	form = ChooseAssignmentForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	return render(request, 'py_grader/submit.html', context)


def submit_assignment(request, assignment_name):
	if request.method == 'POST':
		form = SubmitAssignmentForm(request.POST, request.FILES)
		if form.is_valid():
			get_object_or_404(Assignment, assignment_name=assignment_name)
			try:
				submission_result_id = process_submission(form, assignment_name, request.META['REMOTE_ADDR'])
				return redirect(f'view_submission_result/{submission_result_id}')
			except Exception as e:
				return failure(request, f'submit_assignment/{assignment_name}/', str(e))
		return failure(request, f'submit_assignment/{assignment_name}/', error_list_from_form(form))

	form = SubmitAssignmentForm()
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'form': form,
		'assignment': assignment
	}
	return render(request, 'py_grader/submit_assignment.html', context)


# TODO this should redirect to a result?
@login_required(login_url='/admin')
def test_submit_assignment(request, assignment_name):
	if request.method == 'POST':
		form = SubmitPyFile(request.POST, request.FILES)
		if form.is_valid():
			get_object_or_404(Assignment, assignment_name=assignment_name)
			try:
				process_test_submission(form, assignment_name)
				return success(request, f'test_submit/{assignment_name}/', 'Successfully Test Submitted Assignment')
			except Exception as e:
				return failure(request, f'test_submit/{assignment_name}/', str(e))
		return failure(request, f'test_submit/{assignment_name}/', error_list_from_form(form))

	form = SubmitPyFile()
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'form': form,
		'assignment': assignment
	}
	return render(request, 'py_grader/test_submit_assignment.html', context)


@login_required(login_url='/admin')
def view_results(request):
	if request.method == 'GET':
		form = ChooseAssignmentForm(request.GET)
		if form.is_valid():
			get_object_or_404(Assignment, assigment_name=form.assignment_name)
			return redirect(f'view_assignment_results/{form.assignment_name}/')
		return failure(request, 'view_assignment_results/', error_list_from_form(form))

	form = ChooseAssignmentForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	return render(request, 'py_grader/view_assignment_results.html', context)


# TODO
@login_required(login_url='/admin')
def view_assignment_results(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	return render(request, 'py_grader/view_assignment_results.html', context)


def view_any_submission_result(request):
	if request.method == 'GET':
		form = ViewSubmissionForm(request.GET)
		if form.is_valid():
			get_object_or_404(Submission, pk=form.submission_number)
			return redirect(f'view_submission_result/{form.submission_number}/')
		return failure(request, 'view_assignment_results/', error_list_from_form(form))

	form = ViewSubmissionForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/view_any_submission_result.html', context)


def view_submission_result(request, submission_id):
	submission_result = get_object_or_404(SubmissionResult, submission=submission_id)
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=submission_result.submission.assignment.pk)
	submission_test_cases = [SubmissionCaseResult.objects.get(submission=submission_result.submission.pk, test_case=case.pk) for case in test_cases]
	context = {
		'submission_result': submission_result,
		'submission': submission_result.submission,
		'test_cases': test_cases,
		'submission_test_cases': submission_test_cases
	}
	return render(request, 'py_grader/view_submission_result.html', context)


@login_required(login_url='/admin')
def create_assignment(request):
	if request.method == 'POST':
		form = CreateAssignmentForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				process_assignment(form)
				return success(request, 'create_assignment/', 'Successfully Created Assignment')
			except Exception as e:
				return failure(request, 'create_assignment/', str(e))
		return failure(request, 'create_assignment/', error_list_from_form(form))

	form = CreateAssignmentForm(grading_methods=GradingMethod.objects.all())
	context = {
		'form': form
	}
	return render(request, 'py_grader/create_assignment.html', context)


# TODO
@login_required(login_url='/admin')
def add_test_case(request, assignment_name):
	if request.method == 'POST':
		form = AddTestCaseForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				add_test_case_db(form)
				return success(request, f'add_test_case/{assignment_name}/', 'Successfully Added Test Case')
			except Exception as e:
				return failure(request, f'add_test_case/{assignment_name}/', str(e))
		return failure(request, f'add_test_case/{assignment_name}/', error_list_from_form(form))

	form = AddTestCaseForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	return render(request, 'py_grader/add_test_case.html', context)


@login_required(login_url='/admin')
def manage_net_ids(request):
	context = {
	}
	return render(request, 'py_grader/manage_net_ids.html', context)


@login_required(login_url='/admin')
def add_net_id(request):
	if request.method == 'POST':
		form = NetIDForm(request.POST)
		if form.is_valid():
			try:
				add_net_id_db(form)
				return success(request, 'add_net_id/', 'Successfully Added NetID')
			except Exception as e:
				return failure(request, 'add_net_id/', str(e))
		return failure(request, 'add_net_id/', error_list_from_form(form))

	form = NetIDForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/add_net_id.html', context)


@login_required(login_url='/admin')
def remove_net_id(request):
	if request.method == 'POST':
		form = NetIDForm(request.POST)
		if form.is_valid():
			try:
				remove_net_id_db(form)
				return success(request, 'remove_net_id/', 'Successfully Removed NetID')
			except Exception as e:
				return failure(request, 'remove_net_id/', str(e))
		return failure(request, 'remove_net_id/', error_list_from_form(form))

	form = NetIDForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/remove_net_id.html', context)


@login_required(login_url='/admin')
def upload_net_id_csv(request):
	if request.method == 'POST':
		form = CSVFileForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				num_uploaded = upload_net_id_csv_db(form)
				return success(request, 'upload_net_id_csv/', f'Successfully Uploaded {num_uploaded} NetIDs')
			except Exception as e:
				return failure(request, 'upload_net_id_csv/', str(e))
		return failure(request, 'upload_net_id_csv/', error_list_from_form(form))

	form = CSVFileForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/upload_net_id_csv.html', context)


@login_required(login_url='/admin')
def clear_net_id(request):
	if request.method == 'POST':
		try:
			clear_net_id_db()
			return success(request, 'clear_net_id/', 'Successfully Cleared NetIDs')
		except Exception as e:
			return failure(request, 'clear_net_id/', str(e))

	context = {
	}
	return render(request, 'py_grader/remove_net_id.html', context)


# TODO
def grader_login(request):
	context = {
	}
	return render(request, 'py_grader/grader_login.html', context)


def success(request, back_path, message):
	context = {
		'back_path': back_path,
		'message': message
	}
	return render(request, 'py_grader/success.html', context)


def failure(request, back_path, errors):
	context = {
		'back_path': back_path,
		'errors': errors
	}
	return render(request, 'py_grader/failure.html', context)
