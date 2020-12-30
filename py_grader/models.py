import os

from django.db import models


class GradingMethod(models.Model):
	grading_method = models.CharField(verbose_name='Grading Method', unique=True, max_length=255)


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
	allowed_packages = models.CharField(verbose_name='Allowed Packages', max_length=255)


class NetID(models.Model):
	net_id = models.CharField(verbose_name='NetID', unique=True, max_length=255)


class Submission(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE, verbose_name='NetID')
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	submission_source_code = models.TextField(verbose_name='Source Code')
	submission_time = models.DateTimeField(verbose_name='Submission Time')
	submission_number = models.IntegerField(verbose_name='Submission Number')
	ip_address = models.GenericIPAddressField(verbose_name='Submission IP Address')


class NumberSubmissions(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE, verbose_name='NetID')
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	number_submissions = models.IntegerField(verbose_name='Number Submissions', default=0)


class TestCase(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Assignment')
	test_case_number = models.IntegerField(verbose_name='Test Case Number')
	test_case_input = models.TextField(verbose_name='Test Case Input')
	test_case_output = models.TextField(verbose_name='Test Case Output')


# TODO need to figure out how to get the model working here
class TestCaseFile(models.Model):
	test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='Test Case')
	test_case_file = models.FileField(verbose_name='Test Case File', upload_to=f'test_case_files{os.sep}{test_case_assignment.assignment_name}{os.sep}{test_case.test_case_number}{os.sep}')


class SubmissionCaseResult(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, verbose_name='Submission')
	test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='Test Case')
	test_case_number = models.IntegerField(verbose_name='Test Case Number')
	submission_output = models.TextField(verbose_name='Submission Output')
	expected_output = models.TextField(verbose_name='Expected Output')
	correct = models.BooleanField(verbose_name='Correct')


class SubmissionResult(models.Model):
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, verbose_name='Submission')
	submission_grade = models.FloatField(verbose_name='Submission Grade')
