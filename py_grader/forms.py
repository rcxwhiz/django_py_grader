from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

import py_grader.config as cfg
from py_grader.models import Assignment, NetID, GradingMethod


class CreateAssignmentForm(forms.Form):
	assignment_name = forms.CharField(label='Assignment Name', max_length=255)
	key_source_code = forms.FileField(label='Upload .py File')
	open_time = forms.DateTimeField(label='Open Time', widget=DateTimePickerInput())
	close_time = forms.DateTimeField(label='Close Time', widget=DateTimePickerInput())
	number_submissions = forms.IntegerField(label='Number Submissions Allowed', initial=100, min_value=0)
	grading_method = forms.ModelChoiceField(label='Grading Method', queryset=GradingMethod.objects.all())
	# TODO change this to checkboxes???
	allowed_packages = forms.CharField(label='Allowed Packages (Seperated by Whitespace)', max_length=255,
	                                   required=False)

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
		if code.size > cfg.upload_limit:
			self.add_error('key_source_code', f'File Over {cfg.upload_limit / 1e6} MB')
		open_time = cleaned_data.get('open_time')
		close_time = cleaned_data.get('close_time')
		if open_time > close_time:
			self.add_error('close_time', 'Assignment Must Close After it Opens')
		return cleaned_data


class AddTestCaseForm(forms.Form):
	test_case_input = forms.CharField(label='Test Case argv', widget=forms.Textarea)
	test_case_files = forms.FileField(label='Upload Test Case Files',
	                                  widget=forms.ClearableFileInput(attrs={'multiple': True}))

	def clean(self):
		cleaned_data = super().clean()
		for file in self.files.getlist('test_case_files'):
			if file.size > cfg.upload_limit:
				self.add_error('test_case_files', f'{file.name} Over {cfg.upload_limit / 1e6} MB')
		return cleaned_data


class ChooseAssignmentForm(forms.Form):
	assignment_name = forms.ModelChoiceField(label='Assignment', queryset=Assignment.objects.order_by('close_time'),
	                                         to_field_name='assignment_name')


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
		if code.size > cfg.upload_limit:
			self.add_error('student_source_code', f'File Over {cfg.upload_limit / 1e6} MB')
		return cleaned_data


class SubmitPyFile(forms.Form):
	source_code = forms.FileField(label='Upload a .py File')

	def clean(self):
		cleaned_data = super().clean()
		code = cleaned_data.get('source_code')
		if not code.name.endswith('.py'):
			self.add_error('source_code', 'File Type Must be .py')
		if code.size > cfg.upload_limit:
			self.add_error('student_source_code', f'File Over {cfg.upload_limit / 1e6} MB')
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
		if csv.size > cfg.upload_limit:
			self.add_error('csv_file', f'File Over {cfg.upload_limit / 1e6} MB')
		return cleaned_data
