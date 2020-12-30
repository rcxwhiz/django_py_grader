from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

from py_grader.models import Assignment, NetID


class CreateAssignmentForm(forms.Form):
	assignment_name = forms.CharField(label='Assignment Name', max_length=255)
	key_source_code = forms.FileField(label='Upload .py File')
	open_time = forms.DateTimeField(label='Open Time', widget=DateTimePickerInput())
	close_time = forms.DateTimeField(label='Close Time', widget=DateTimePickerInput())
	number_submissions = forms.IntegerField(label='Number Submissions Allowed', initial=100, min_value=0)
	grading_method = forms.ChoiceField(label='Grading Method', choices=[])
	allowed_pacakges = forms.CharField(label='Allowed Packages (Seperated by Whitespace)', max_length=255,
	                                   required=False)

	def __init__(self, grading_methods=None, *args, **kwargs):
		super(CreateAssignmentForm, self).__init__(*args, **kwargs)
		if grading_methods:
			grading_choices = []
			for grading_method in grading_methods:
				grading_choices.append((grading_method.pk, grading_method.grading_method))
			self.fields['grading_method'].choices = grading_choices

	def clean(self):
		cleaned_data = super().clean()
		assignment_name = cleaned_data.get('assignment_name')
		try:
			Assignment.objects.get(assignment_name=assignment_name)
			self.add_error('assignment_name', 'Assignment Name Already Used')
		except Assignment.DoesNotExist:
			pass
		code = cleaned_data.get('key_source_code')
		if not code.name.endswith('.py'):
			self.add_error('key_source_code', 'File Type Must be .py')
		if code.size > 4e6:
			self.add_error('key_source_code', 'File Over 4 MB')
		open_time = cleaned_data.get('open_time')
		close_time = cleaned_data.get('close_time')
		if open_time > close_time:
			self.add_error('close_time', 'Assignment Must Close After it Opens')
		return cleaned_data


class AddTestCaseForm(forms.Form):
	assignment_name = forms.ChoiceField(label='Assignment', choices=[])
	test_case_input = forms.CharField(label='Test Case argv', widget=forms.Textarea)
	test_case_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

	def __init__(self, assignments=None, *args, **kwargs):
		super(AddTestCaseForm, self).__init__(*args, **kwargs)
		if assignments:
			assignment_choices = []
			for i in range(len(assignments)):
				assignment_choices.append((i + 1, assignments[i].assignment_name))
			self.fields['assignment_name'].choices = assignment_choices

	def clean(self):
		cleaned_data = super().clean()
		for file in cleaned_data.getlist('test_case_files'):
			if file.size > 4e6:
				self.add_error('test_case_files', f'{file.name} Over 4 MB')
		return cleaned_data


class ChooseAssignmentForm(forms.Form):
	assignment_name = forms.ChoiceField(label='Assignment', choices=[])

	def __init__(self, assignments=None, *args, **kwargs):
		super(ChooseAssignmentForm, self).__init__(*args, **kwargs)
		if assignments:
			assignment_choices = []
			for i in range(len(assignments)):
				assignment_choices.append((i + 1, assignments[i].assignment_name))
			self.fields['assignment_name'].choices = assignment_choices


class SubmitAssignmentForm(forms.Form):
	net_id = forms.CharField(label='NetID', max_length=255)
	student_source_code = forms.FileField(label='Upload .py File')

	def clean(self):
		cleaned_data = super().clean()
		net_id = cleaned_data.get('net_id')
		try:
			NetID.objects.get(net_id=net_id)
		except NetID.DoesNotExist:
			self.add_error('net_id', 'NetID Not Found')
		code = cleaned_data.get('student_source_code')
		if not code.name.endswith('.py'):
			self.add_error('student_source_code', 'File Type Must be .py')
		if code.size > 4e6:
			self.add_error('student_source_code', 'File over 4MB')
		return cleaned_data


class SubmitPyFile(forms.Form):
	source_code = forms.FileField(label='Upload a .py File')

	def clean(self):
		cleaned_data = super().clean()
		code = cleaned_data.get('source_code')
		if not code.name.endswith('.py'):
			self.add_error('source_code', 'File Type Must be .py')
		if code.size > 4e6:
			self.add_error('student_source_code', 'File Over 4MB')
		return cleaned_data


class ViewSubmissionForm(forms.Form):
	submission_number = forms.IntegerField(label='Submission ID', min_value=0)


class AddGradingMethodForm(forms.Form):
	grading_method = forms.CharField(label='Grading Method', max_length=255)


class NetIDNameForm(forms.Form):
	net_id = forms.CharField(label='NetID', max_length=255)
	name = forms.CharField(label='Name', max_length=255, required=False)
	first_name = forms.CharField(label='First Name', max_length=255, required=False)
	last_name = forms.CharField(label='Last Name', max_length=255, required=False)


class NetIDForm(forms.Form):
	net_id = forms.CharField(label='NetID', max_length=255)


class CSVFileForm(forms.Form):
	csv_file = forms.FileField(label='Upload a .csv File')

	def clean(self):
		cleaned_data = super().clean()
		csv = cleaned_data.get('csv_file')
		if not csv.name.endswith('.csv'):
			self.add_error('csv_file', 'File Type Must be .csv')
		if csv.size > 4e6:
			self.add_error('csv_file', 'File Over 4MB')
		return cleaned_data
