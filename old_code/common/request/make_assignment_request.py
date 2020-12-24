from old_code.common.model.assignment import Assignment


class MakeAssigmentRequest:
	def __init__(self, assignment: Assignment):
		self.assignment: Assignment = assignment
