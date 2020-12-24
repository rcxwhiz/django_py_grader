from common.model.test_case import TestCase


class MakeTestCaseRequest:
	def __init__(self, test_case: TestCase):
		self.test_case: TestCase = test_case
