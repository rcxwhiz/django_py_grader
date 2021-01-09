def error_list_from_form(form):
	msgs = []
	for key in form.errors.as_data():
		for err in form.errors.as_data()[key]:
			msgs.append(f'{key}: {err.message}')
	return '\n'.join(msgs)
