from old_code.common import NetId


class GetAssignmentGradesRequest:
	def __init__(self, net_id: NetId, assignment_name: str):
		self.net_id: NetId = net_id
		self.assignment_name: str = assignment_name
