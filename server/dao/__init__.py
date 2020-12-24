database_path = 'py_grader.db'

# == assignments table ==
assignments_table = 'assignments'
assignment_name_column = 'assignment_name'
assignment_key_code_column = 'key_code'
assignment_open_time_column = 'open_time'
assignment_close_time_column = 'close_time'
total_submissions_column = 'total_submissions'
total_unique_submissions_column = 'total_unique_submissions'
number_allowed_submissions_column = 'number_allowed_submissions'
number_test_cases_column = 'number_test_cases'
grading_method_column = 'grading_method'

# == net ids table ==
net_ids_table = 'net_ids'
net_id_column = 'net_id'

# == submissions table ==
submissions_table = 'submissions'
# net_id_column
# assignment_name_column
submission_code_column = 'submission_code'
submission_time_column = 'submission_time'

# == number submissions table ==
number_submissions_table = 'number_submissions'
# net_id_column
# assignment_name_column
number_submissions_column = 'number_submissions'

# == submission results table ==
submission_results_table = 'submission_results'
# net_id_column
# assignment_name_column
# submission_code_column
# submission_time_column
submission_number_column = 'submission_number'
submission_grade_column = 'submission_grade'

# == submission case result table ==
submission_case_results_table = 'submission_case_results'
# net_id_column
# assignment_name_column
# test_case_number_column
submission_output_column = 'submission_output'
correct_column = 'correct_column'

# == test cases table ==
test_case_table = 'test_cases'
# assignment_name_column
test_case_number_column = 'test_case_number'
test_case_stdin_column = 'test_case_stdin'
test_case_argv_column = 'test_case_argv'
test_case_output_column = 'test_case_output'

from server.dao.assignments_dao import AssignmentsDao
from server.dao.netid_dao import NetIdDao
from server.dao.number_submissions_dao import NumberSubmissionsDao
from server.dao.submission_case_results_dao import SubmissionCaseResultsDao
from server.dao.submission_results_dao import SubmissionResultsDao
from server.dao.submissions_dao import SubmissionsDao
from server.dao.test_cases_dao import TestCasesDao


# reset all tables
if __name__ == '__main__':
	assignments_dao = AssignmentsDao()
	assignments_dao.reset_table()

	net_id_dao = NetIdDao()
	net_id_dao.reset_table()

	number_submissions_dao = NumberSubmissionsDao()
	number_submissions_dao.reset_table()

	submission_case_results_dao = SubmissionCaseResultsDao()
	submission_case_results_dao.reset_table()

	submission_results_dao = SubmissionResultsDao()
	submission_results_dao.reset_table()

	submissions_dao = SubmissionsDao()
	submissions_dao.reset_table()

	test_cases_dao = TestCasesDao()
	test_cases_dao.reset_table()
