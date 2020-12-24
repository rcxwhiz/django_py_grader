from common.model.submission import Submission


class SubmitAssignmentRequest:
	def __init__(self, submission: Submission):
		self.submission: Submission = submission
