from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from py_grader.handler import process_assignment, process_submission
from py_grader.forms import CreateAssignmentForm, SubmitAssignmentForm
from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase, GradingMethod
from py_grader.util import error_list_from_form


# TODO
def index(request):
	context = {
	}
	return render(request, 'py_grader/index.html', context)


# TODO
def submit(request):
	assignments = Assignment.objects.order_by('close_time')
	context = {
		'assignments': assignments
	}
	return render(request, 'py_grader/submit.html', context)


def submit_assignment(request, assignment_name):
	if request.method == 'POST':
		form = SubmitAssignmentForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				process_submission(form, assignment_name, request.META['REMOTE_ADDR'])
				return success(request, f'submit_assignment/{assignment_name}/', 'Successfully Submitted Assignment')
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


# TODO
@login_required(login_url='/admin')
def test_submit_assignment(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	return render(request, 'py_grader/test_submit_assignment.html', context)


# TODO
@login_required(login_url='/admin')
def view_results(request):
	assignments = Assignment.objects.order_by('close_time')
	context = {
		'assignments': assignments
	}
	return render(request, 'py_grader/view_results.html', context)


# TODO
@login_required(login_url='/admin')
def view_assignment_results(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	return render(request, 'py_grader/view_assignment_results.html', context)


# TODO
def view_any_submission_result(request):
	context = {
	}
	return render(request, 'py_grader/view_any_submission_result.html', context)


# TODO
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

	form = CreateAssignmentForm()
	context = {
		'form': form
	}
	return render(request, 'py_grader/create_assignment.html', context)


# TODO
@login_required(login_url='/admin')
def manage_net_ids(request):
	context = {
	}
	return render(request, 'py_grader/manage_net_ids.html', context)


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
