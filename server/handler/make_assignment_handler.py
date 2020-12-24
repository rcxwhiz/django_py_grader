from server.dao import AssignmentsDao, TestCasesDao
from common.request import MakeAssigmentRequest
from common.response.make_assignment_response import MakeAssignmentResponse


class MakeAssignmentHandler:

	def make_assignment(self, request: MakeAssigmentRequest) -> MakeAssignmentResponse:
		assignment_dao = AssignmentsDao()
		test_cases_dao = TestCasesDao()
