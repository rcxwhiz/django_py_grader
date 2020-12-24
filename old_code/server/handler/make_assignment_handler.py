from old_code.server.dao import AssignmentsDao, TestCasesDao
from old_code.common import MakeAssigmentRequest
from old_code.common.response import MakeAssignmentResponse


class MakeAssignmentHandler:

	def make_assignment(self, request: MakeAssigmentRequest) -> MakeAssignmentResponse:
		assignment_dao = AssignmentsDao()
		test_cases_dao = TestCasesDao()
