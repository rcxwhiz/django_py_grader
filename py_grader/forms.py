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
	choices = []
	for i in range(len(grading_methods)):
		choices.append((i + 1, grading_methods[i].grading_method))
	grading_method = forms.ChoiceField(label='Grading Method', choices=choices)

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
