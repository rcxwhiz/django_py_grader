from django.db import models

from py_grader.model.assignment import GradingMethod


class Assignment(models.Model):
	assignment_name = models.CharField(max_length=200)
	key_source_code = models.TextField()
	open_time = models.DateTimeField()
	close_time = models.DateTimeField()
	total_submissions = models.IntegerField(default=0)
	number_students_submited = models.IntegerField(default=0)
	number_submissions_allowed = models.IntegerField(default=100)
	number_test_cases = models.IntegerField(default=0)
	grading_method = models.IntegerField(default=GradingMethod.num_all_tests_cases)


class NetID(models.Model):
	net_id = models.CharField(max_length=255)


class NumberSubmissions(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE)
	assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	number_submissions = models.IntegerField(default=0)


class SubmissionCaseResult(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE)
	assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	test_case_number = models.IntegerField()
	submission_output = models.TextField()
	submission_case_correct = models.BooleanField()


class SubmissionResult(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE)
	assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	submission_number = models.IntegerField()
	submission_grade = models.FloatField()


class Submission(models.Model):
	net_id = models.ForeignKey(NetID, on_delete=models.CASCADE)
	assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	submission_code = models.TextField()
	submission_time = models.DateTimeField()
	submission_number = models.IntegerField()


class TestCase(models.Model):
	assignment_name = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	test_case_number = models.IntegerField()
	test_case_input = models.TextField()
	test_case_output = models.TextField()
