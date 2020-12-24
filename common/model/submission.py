from common.model.net_id import NetId


class Submission:
	def __init__(self, net_id: NetId, assignment_name: str, submission_source_code: str, submission_time: int):
		# the NetID of the student submitting
		self.net_id: NetId = net_id
		# the name of the assignment being submitted
		self.assignment_name: str = assignment_name
		# the code the student is submitting
		self.submission_source_code: str = submission_source_code
		# the time the student is making the submission
		self.submission_time: int = submission_time
