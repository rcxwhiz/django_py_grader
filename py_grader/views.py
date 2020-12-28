from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from py_grader.handler import process_assignment, process_submission, process_test_submission
from py_grader.forms import CreateAssignmentForm, SubmitAssignmentForm, ChooseAssignmentForm, SubmitPyFile, \
	ViewSubmissionForm, NetIDForm
from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase, GradingMethod, Submission, \
	NetID
from py_grader.util import error_list_from_form


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
		return failure('submit/', error_list_from_form(form))

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
				return failure(f'submit_assignment/{assignment_name}/', str(e))
		return failure(f'submit_assignment/{assignment_name}/', error_list_from_form(form))

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
				return success(f'test_submit/{assignment_name}/', 'Successfully Test Submitted Assignment')
			except Exception as e:
				return failure(f'test_submit/{assignment_name}/', str(e))
		return failure(f'test_submit/{assignment_name}/', error_list_from_form(form))

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
		return failure('view_assignment_results/', error_list_from_form(form))

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
		return failure('view_assignment_results/', error_list_from_form(form))

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
				return success('create_assignment/', 'Successfully Created Assignment')
			except Exception as e:
				return failure('create_assignment/', str(e))
		return failure('create_assignment/', error_list_from_form(form))

	form = CreateAssignmentForm(grading_methods=GradingMethod.objects.all())
	context = {
		'form': form
	}
	return render(request, 'py_grader/create_assignment.html', context)


# TODO
@login_required(login_url='/admin')
def add_test_case(request, assignment_name):
	context = {
	}
	return render(request, 'py_grader/add_test_case.html', context)


@login_required(login_url='/admin')
def manage_net_ids(request):
	context = {
	}
	return render(request, 'py_grader/manage_net_ids.html', context)


# TODO
@login_required(login_url='/admin')
def add_net_id(request):
	if request.method == 'POST':
		form = NetIDForm(request.POST)
		if form.is_valid():
			get_object_or_404(NetID, net_id=form.net_id)
			add_net_id_db(form)
			return success('add_net_id/', 'Successfully Added NetID')
		return failure('add_net_id/', error_list_from_form(form))

	form = NetIDForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/add_net_id.html', context)


# TODO
@login_required(login_url='/admin')
def remove_net_id(request):
	context = {
	}
	return render(request, 'py_grader/remove_net_id.html', context)


# TODO
@login_required(login_url='/admin')
def upload_net_id_csv(request):
	context = {
	}
	return render(request, 'py_grader/upload_net_id_csv.html', context)


# TODO
@login_required(login_url='/admin')
def clear_net_id(request):
	context = {
	}
	return render(request, 'py_grader/clear_net_id.html', context)


# TODO
def grader_login(request):
	context = {
	}
	return render(request, 'py_grader/grader_login.html', context)


def success(back_path, message):
	context = {
		'back_path': back_path,
		'message': message
	}
	return redirect('py_grader/success.html', context)


def failure(back_path, errors):
	context = {
		'back_path': back_path,
		'errors': errors
	}
	return redirect('py_grader/failure.html', context)
