from py_grader.model.net_id import NetId


class SubmissionResult:
	def __init__(self, net_id: NetId,
	             assignment_name: str,
	             submission_source_code: str,
	             submission_time: int,
	             submission_number: int,
	             submission_grade: float,
	             runtime: float):
		# the NetID of the student the result is for
		self.net_id: NetId = net_id
		# the name of the assignment
		self.assignment_name: str = assignment_name
		# the code the student submitted
		self.submission_source_code: str = submission_source_code
		# the time of the submission
		self.submission_time: int = submission_time
		# the number submission this was for this assignment for this student
		self.submission_number: int = submission_number
		# the grade the student got on this assignment
		self.submission_grade: float = submission_grade
		# the time it took for this code to run on the grader
		self.runtime: float = runtime
