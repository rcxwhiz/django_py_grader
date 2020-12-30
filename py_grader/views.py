from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from py_grader.forms import CreateAssignmentForm, SubmitAssignmentForm, ChooseAssignmentForm, SubmitPyFile, \
	ViewSubmissionForm, NetIDNameForm, CSVFileForm, AddTestCaseForm, NetIDForm
from py_grader.handler import process_assignment, process_submission, process_test_submission, add_net_id_db, \
	remove_net_id_db, clear_net_id_db, upload_net_id_csv_db, add_test_case_db
from py_grader.models import Assignment, SubmissionResult, SubmissionCaseResult, TestCase, GradingMethod, Submission
from py_grader.util import error_list_from_form


def index(request):
	context = {
	}
	return render(request, 'py_grader/index.html', context)


def grader_index(request):
	context = {
	}
	return render(request, 'py_grader/grader_index.html', context)


def submit(request, success_message=None, failure_message=None):
	form = ChooseAssignmentForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/submit.html', context)


def submit_get(request):
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		get_object_or_404(Assignment, assignment_name=form.assignment_name)
		return redirect(f'submit/{form.assignment_name}/')
	return submit(request, failure_message=error_list_from_form(form))


def submit_assignment(request, assignment_name, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = SubmitAssignmentForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			get_object_or_404(Assignment, assignment_name=assignment_name)
			try:
				submission_result_id = process_submission(form, assignment_name, request.META['REMOTE_ADDR'])
				return redirect(f'view_submission_result/{submission_result_id}')
			except Exception as e:
				return submit_assignment(request, assignment_name, failure_message=str(e))
		return submit_assignment(request, assignment_name, failure_message=error_list_from_form(form))

	form = SubmitAssignmentForm()
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'form': form,
		'assignment': assignment
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/submit_assignment.html', context)


# TODO this should redirect to a result?
@login_required(redirect_field_name=f'/grader')
def test_submit_assignment(request, assignment_name, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = SubmitPyFile(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			get_object_or_404(Assignment, assignment_name=assignment_name)
			try:
				process_test_submission(form, assignment_name)
				return test_submit_assignment(request, assignment_name, success_message='Successfully Submitted Test Assignment')
			except Exception as e:
				return test_submit_assignment(request, assignment_name, failure_message=str(e))
		return test_submit_assignment(request, assignment_name, failure_message=error_list_from_form(form))

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


@login_required(redirect_field_name=f'/grader')
def view_results(request, success_message=None, failure_message=None):
	form = ChooseAssignmentForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_assignment_results.html', context)


def view_results_get(request):
	form = ChooseAssignmentForm(request.GET)
	if form.is_valid():
		get_object_or_404(Assignment, assigment_name=form.assignment_name)
		return redirect(f'view_assignment_results/{form.assignment_name}/')
	return view_results(request, failure_message=error_list_from_form(form))


# TODO
@login_required(redirect_field_name=f'/grader')
def view_assignment_results(request, assignment_name, success_message=None, failure_message=None):
	assignment = get_object_or_404(Assignment, assignment_name=assignment_name)
	context = {
		'assignment': assignment
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_assignment_results.html', context)


def view_any_submission_result(request, success_message=None, failure_message=None):
	form = ViewSubmissionForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/view_any_submission_result.html', context)


def view_any_submission_result_get(request):
	form = ViewSubmissionForm(request.GET)
	if form.is_valid():
		get_object_or_404(Submission, pk=form.submission_number)
		return redirect(f'view_submission_result/{form.submission_number}/')
	return view_any_submission_result(request, failure_message=error_list_from_form(form))


def view_submission_result(request, submission_id, success_message=None, failure_message=None):
	submission_result = get_object_or_404(SubmissionResult, submission=submission_id)
	test_cases = TestCase.objects.order_by('test_case_number').filter(assignment=submission_result.submission.assignment.pk)
	submission_test_cases = [SubmissionCaseResult.objects.get(submission=submission_result.submission.pk, test_case=case.pk) for case in test_cases]
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


@login_required(redirect_field_name=f'/grader')
def create_assignment(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = CreateAssignmentForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			try:
				process_assignment(form)
				return create_assignment(request, success_message='Successfully Created Assignment')
			except Exception as e:
				return create_assignment(request, failure_message=str(e))
		return create_assignment(request, failure_message=error_list_from_form(form))

	form = CreateAssignmentForm(grading_methods=GradingMethod.objects.all())
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/create_assignment.html', context)


@login_required(redirect_field_name=f'/grader')
def add_test_case(request, assignment_name, success_message=None, failure_message=None):
	get_object_or_404(Assignment, assignment_name=assignment_name)
	if request.method == 'POST':
		form = AddTestCaseForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			try:
				add_test_case_db(form)
				return add_test_case(request, assignment_name, success_message='Successfully Added Test Case')
			except Exception as e:
				return add_test_case(request, assignment_name, str(e))
		return add_test_case(request, assignment_name, error_list_from_form(form))

	form = AddTestCaseForm(assignments=Assignment.objects.order_by('close_time'))
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/add_test_case.html', context)


@login_required(redirect_field_name=f'/grader')
def manage_net_ids(request, success_message=None, failure_message=None):
	context = {
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/manage_net_ids.html', context)


@login_required(redirect_field_name=f'/grader')
def add_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = NetIDNameForm(request.POST)
		request.method = 'GET'
		if form.is_valid():
			try:
				add_net_id_db(form)
				return add_net_id(request, success_message='Successfully Added NetID')
			except Exception as e:
				return add_net_id(request, failure_message=str(e))
		return add_net_id(request, failure_message=error_list_from_form(form))

	form = NetIDNameForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/add_net_id.html', context)


@login_required(redirect_field_name=f'/grader')
def remove_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = NetIDForm(request.POST)
		request.method = 'GET'
		if form.is_valid():
			try:
				remove_net_id_db(form)
				return remove_net_id(request, success_message='Successfully Removed NetID')
			except Exception as e:
				return remove_net_id(request, failure_message=str(e))
		return remove_net_id(request, failure_message=error_list_from_form(form))

	form = NetIDForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/remove_net_id.html', context)


@login_required(redirect_field_name=f'/grader')
def upload_net_id_csv(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		form = CSVFileForm(request.POST, request.FILES)
		request.method = 'GET'
		if form.is_valid():
			try:
				num_uploaded = upload_net_id_csv_db(form)
				return upload_net_id_csv(request, success_message=f'Successfully Uploaded {num_uploaded} NetIDs')
			except Exception as e:
				return upload_net_id_csv(request, failure_message=str(e))
		return upload_net_id_csv(request, failure_message=error_list_from_form(form))

	form = CSVFileForm()
	context = {
		'form': form
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/upload_net_id_csv.html', context)


@login_required(redirect_field_name=f'/grader')
def clear_net_id(request, success_message=None, failure_message=None):
	if request.method == 'POST':
		request.method = 'GET'
		try:
			clear_net_id_db()
			return clear_net_id(request, success_message='Successfully Cleared NetIDs')
		except Exception as e:
			return clear_net_id(request, failure_message=str(e))

	context = {
	}
	if success_message:
		context['success_message'] = success_message
	if failure_message:
		context['failure_message'] = failure_message
	return render(request, 'py_grader/remove_net_id.html', context)
