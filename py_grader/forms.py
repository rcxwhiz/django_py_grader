from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

from py_grader.models import GradingMethod


class CreateAssignmentForm(forms.Form):
	assignment_name = forms.CharField(label='Assignment Name', max_length=255)
	key_source_code = forms.FileField(label='Upload .py File')
	open_time = forms.DateTimeField(label='Open Time', widget=DateTimePickerInput())
	close_time = forms.DateTimeField(label='Close Time', widget=DateTimePickerInput())
	number_submissions = forms.IntegerField(label='Number Submissions Allowed', initial=100, min_value=0)
	grading_methods = GradingMethod.objects.all()
	choices = []
	for i in range(len(grading_methods)):
		choices.append((i + 1, grading_methods[i].grading_method))
	grading_method = forms.ChoiceField(label='Grading Method', choices=choices)
