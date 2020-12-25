from django.shortcuts import render, get_object_or_404

from py_grader.models import Assignment


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
