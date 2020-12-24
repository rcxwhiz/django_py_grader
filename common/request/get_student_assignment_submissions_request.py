from common.model.net_id import NetId


class GetStudentAssignmentSubmissionRequest:
	def __init__(self, net_id: NetId, assignment_name: str):
		self.net_id: NetId = net_id
		self.assignment_name: str = assignment_name
