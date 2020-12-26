from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

from py_grader.models import GradingMethod, Assignment


class CreateAssignmentForm(forms.Form):
	assignment_name = forms.CharField(label='Assignment Name', max_length=255)
	key_source_code = forms.FileField(label='Upload .py File')
	open_time = forms.DateTimeField(label='Open Time', widget=DateTimePickerInput())
	close_time = forms.DateTimeField(label='Close Time', widget=DateTimePickerInput())
	number_submissions = forms.IntegerField(label='Number Submissions Allowed', initial=100, min_value=0)
	grading_methods = GradingMethod.objects.all()
	grading_choices = []
	for i in range(len(grading_methods)):
		grading_choices.append((i + 1, grading_methods[i].grading_method))
	grading_method = forms.ChoiceField(label='Grading Method', choices=grading_choices)

	def clean(self):
		cleaned_data = super().clean()
		assignment_name = cleaned_data.get('assignment_name')
		try:
			Assignment.objects.get(assignment_name=assignment_name)
			self.add_error('assignment_name', 'Assignment Name Already Used')
		except Assignment.DoesNotExist:
			pass
		open_time = cleaned_data.get('open_time')
		close_time = cleaned_data.get('close_time')
		if open_time > close_time:
			self.add_error('close_time', 'Assignment Must Close After it Opens')
		return self.cleaned_data


class AddTestCaseForm(forms.Form):
	assignment_choices = []
	assignments = Assignment.objects.order_by('close_time')
	for i in range(len(assignments)):
		assignment_choices.append((i + 1, assignments[i].assignment_name))
	assignment_name = forms.ChoiceField(label='Assignment', choices=assignment_choices)
	test_case_input = forms.CharField(label='Test Case Input', widget=forms.Textarea)


class SubmitAssignmentForm(forms.Form):
	net_id = forms.CharField(label='NetID', max_length=255)
	student_source_code = forms.FileField(label='Upload .py File')


class ViewSubmissionForm(forms.Form):
	submission_number = forms.IntegerField(label='Submission ID', min_value=0)


class ViewAssignmentResultForm(forms.Form):
	assignment_choices = []
	assignments = Assignment.objects.order_by('close_time')
	for i in range(len(assignments)):
		assignment_choices.append((i + 1, assignments[i].assignment_name))
	assignment_name = forms.ChoiceField(label='Assignment', choices=assignment_choices)


class AddGradingMethodForm(forms.Form):
	grading_method = forms.CharField(label='Grading Method', max_length=255)
