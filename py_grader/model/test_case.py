class TestCase:
	def __init__(self, assignment_name: str,
	             test_case_number: int,
	             test_case_stdin: str,
	             test_case_argv: str,
	             test_case_output: str):
		# the name of the assignment for this test case
		self.assignment_name: str = assignment_name
		# the test case number for this case
		self.test_case_number: int = test_case_number
		# the stdin for this test case
		self.test_case_stdin: str = test_case_stdin
		# the argv for this test case represented as a string
		self.test_case_argv: str = test_case_argv
		# the output for this test case
		self.test_case_output: str = test_case_output
