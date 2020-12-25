from django.shortcuts import render, get_object_or_404

from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, Submission, TestCase


def index(request):
	context = {
	}
	return render(request, 'py_grader/index.html', context)


def submit(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment.assignment_name
	}
	return render(request, 'py_grader/submit.html', context)


def create(request):
	context = {
	}
	return render(request, 'py_grader/create.html', context)


def view_results(request, assignment_name):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment.assignment_name
	}
	return render(request, 'py_grader/view_results.html', context)


def view_result(request, submission_id):
	submission_result = get_object_or_404(SubmissionResult, submission=submission_id)
	submission = get_object_or_404(Submission, pk=submission_result.submission.pk)
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=submission.assignment.pk)
	submission_test_cases = [SubmissionCaseResult.objects.filter(submission=submission.pk, test_case=case.pk) for case in test_cases]
	context = {
		'submission_result': submission_result,
		'submission': submission,
		'test_cases': test_cases,
		'submission_test_cases': submission_test_cases
	}
	return render(request, 'py_grader/view_result.html', context)
