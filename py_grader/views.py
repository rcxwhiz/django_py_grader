from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase

# TODO any of these pages that require redirection don't go to their thing after you log in


# TODO this is a very temporary setup as well
# TODO I want to add a dropdown to this page that lets you choose an assignment to submit_assignment
def index(request):
	context = {
	}
	return render(request, 'py_grader/index.html', context)


def submit(request):
	assignments = Assignment.objects.order_by('close_time')
	context = {
		'assignments': assignments
	}
	return render(request, 'py_grader/submit.html', context)


def submit_assignment(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	return render(request, 'py_grader/submit_assignment.html', context)


def create(request):
	return redirect('/admin/py_grader/assignment/add')


@login_required(login_url='/admin')
def view_results(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	return render(request, 'py_grader/view_results.html', context)


# TODO this is a very temporary mockup
def view_result(request, submission_id):
	submission_result = get_object_or_404(SubmissionResult, submission=submission_id)
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=submission_result.submission.assignment.pk)
	submission_test_cases = [SubmissionCaseResult.objects.get(submission=submission_result.submission.pk, test_case=case.pk) for case in test_cases]
	context = {
		'submission_result': submission_result,
		'submission': submission_result.submission,
		'test_cases': test_cases,
		'submission_test_cases': submission_test_cases
	}
	return render(request, 'py_grader/view_result.html', context)
