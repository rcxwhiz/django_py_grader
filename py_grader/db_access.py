from py_grader.models import Assignment, GradingMethod


def process_assignment(form):
	assignment = Assignment()
	data = form.cleaned_data
	assignment.assignment_name = data.get('assignment_name')
	in_memory_code = data.get('key_source_code')
	code_text = ''
	for line in in_memory_code:
		code_text += line.decode()
	assignment.key_source_code = code_text
	assignment.open_time = data.get('open_time')
	assignment.close_time = data.get('close_time')
	assignment.total_submissions = 0
	assignment.number_students_submited = 0
	assignment.number_submissions_allowed = data.get('number_submissions')
	assignment.number_test_cases = 0
	assignment.grading_method = GradingMethod.objects.get(pk=data.get('grading_method'))
	assignment.save()
