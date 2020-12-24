from old_code.common import NetId


class GetStudentSubmissionRequest:
	def __init__(self, net_id: NetId, assignment_name: str, submission_source_code: str):
		self.net_id: NetId = net_id
		self.assigment_name: str = assignment_name
		self.submission_source_code: str = submission_source_code
