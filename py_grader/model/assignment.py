from enum import Enum


class GradingMethod(Enum):
	completion = 1
	all_or_nothing = 2
	num_all_tests_cases = 3
	num_all_test_cases_sequential = 4


class Assignment:
	def __init__(self, name: str,
	             key_source_code: str,
	             open_time: int,
	             close_time: int,
	             total_submissions: int,
	             total_unique_submissions: int,
	             number_allowed_submissions: int,
	             number_test_cases: int,
	             grading_method: GradingMethod):
		# the name of the assignment
		self.name: str = name
		# code that correctly solves the assignment
		self.key_source_code: str = key_source_code
		# the time the assignment opens
		self.open_time: int = open_time
		# the time the assignment closes
		self.close_time: int = close_time
		# the number of times students have made submissions to this assignment
		self.total_submissions: int = total_submissions
		# the number of different students who have made a submission to the assignment
		self.total_unique_submissions: int = total_unique_submissions
		# the number of submissions a student is allowed to make on this assignment
		self.number_allowed_submissions: int = number_allowed_submissions
		# the number of test cases this assignment uses
		self.number_test_cases: int = number_test_cases
		# the grading method to be used on the assignment
		self.grading_method: GradingMethod = grading_method
