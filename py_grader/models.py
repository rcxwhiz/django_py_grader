import logging
import os

from django.db import models

logger = logging.getLogger(__name__)


class GradingMethod(models.Model):
	grading_method = models.CharField(verbose_name='Grading Method', unique=True, max_length=255)

	def __str__(self):
		return self.grading_method


class Assignment(models.Model):
	assignment_name = models.CharField(verbose_name='Assignment Name', unique=True, max_length=255)
	key_source_code = models.TextField(verbose_name='Source Code')
	open_time = models.DateTimeField(verbose_name='Open Time')
	close_time = models.DateTimeField(verbose_name='Close Time')
	total_submissions = models.IntegerField(verbose_name='Total Submissions', default=0)
	number_students_submited = models.IntegerField(verbose_name='Number of Students Submitted', default=0)
	number_submissions_allowed = models.IntegerField(verbose_name='Number Submissions Allowed', default=100)
	number_test_cases = models.IntegerField(verbose_name='Number Test Cases', default=0)
	grading_method = models.ForeignKey(GradingMethod, on_delete=models.PROTECT, verbose_name='Grading Method')
	allowed_packages = models.CharField(verbose_name='Allowed Packages', max_length=255, blank=True, null=True)

	def __str__(self):
		return self.assignment_name


class NetID(models.Model):
	net_id = models.CharField(verbose_name='NetID', unique=True, max_length=255)
	name = models.CharField(verbose_name='Name', blank=True, max_length=255)
	first_name = models.CharField(verbose_name='First Name', blank=True, max_length=255)
	last_name = models.CharField(verbose_name='Last Name', blank=True, max_length=255)

	def __str__(self):
		return self.net_id


class Submission(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE, verbose_name='NetID')
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	submission_source_code = models.TextField(verbose_name='Source Code')
	submission_time = models.DateTimeField(verbose_name='Submission Time')
	submission_number = models.IntegerField(verbose_name='Submission Number')
	ip_address = models.GenericIPAddressField(verbose_name='Submission IP Address')

	def __str__(self):
		return f'{self.assignment} - {self.net_id} ({self.submission_number})'


class NumberSubmissions(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE, verbose_name='NetID')
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	number_submissions = models.IntegerField(verbose_name='Number Submissions', default=0)

	def __str__(self):
		return f'{self.assignment} - {self.net_id} - {self.number_submissions}'


class TestCase(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	test_case_number = models.IntegerField(verbose_name='Test Case Number')
	test_case_input = models.TextField(verbose_name='Test Case Input')
	test_case_output = models.TextField(verbose_name='Test Case Output')

	def __str__(self):
		return f'{self.assignment} ({self.test_case_number})'


def content_file_name(test_case_file, filename):
	logger.debug(f'Getting a filname for {filename} in {test_case_file.test_case.assignment}')
	return os.sep.join(['test_case_files', test_case_file.test_case.assignment.assignment_name,
	                    str(test_case_file.test_case.test_case_number), filename])


class TestCaseFile(models.Model):
	test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='Test Case')
	test_case_file = models.FileField(verbose_name='Test Case File', upload_to=content_file_name)

	def __str__(self):
		return f'{self.test_case} - {self.test_case_file.name}'


class SubmissionCaseResult(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, verbose_name='Submission')
	test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='Test Case')
	test_case_number = models.IntegerField(verbose_name='Test Case Number')
	submission_output = models.TextField(verbose_name='Submission Output')
	expected_output = models.TextField(verbose_name='Expected Output')
	correct = models.BooleanField(verbose_name='Correct')

	def __str__(self):
		return f'{self.submission} ({self.test_case_number}) - ({self.correct})'


class SubmissionResult(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, verbose_name='Submission')
	# TODO I thought that an int would be better here
	submission_grade = models.FloatField(verbose_name='Submission Grade')

	def __str__(self):
		return f'{self.submission} - {self.submission_grade}%'
