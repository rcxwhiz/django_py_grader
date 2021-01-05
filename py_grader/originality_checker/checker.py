from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Expecting a list of tuples with identifier and then code string
# Returns a list of tuples with identifier identifier score
def check_file_set(student_submissions):
	student_ids = [student_submission[0] for student_submission in student_submissions]
	student_code = [student_submission[1] for student_submission in student_submissions]

	vectorize = lambda text: TfidfVectorizer().fit_transform(text).toarray()
	similarity = lambda file1, file2: cosine_similarity([file1, file2])

	vectors = vectorize(student_code)
	s_vectors = list(zip(student_ids, vectors))

	plagiarism_results = set()
	for student_a, text_student_a in s_vectors:
		new_vectors = s_vectors.copy()
		current_index = new_vectors.index((student_a, text_student_a))
		del new_vectors[current_index]
		for student_b, text_student_b in new_vectors:
			sim_score = similarity(text_student_a, text_student_b)[0][1]
			student_pair = sorted((student_a, student_b))
			score = (student_pair[0], student_pair[1], sim_score)
			plagiarism_results.add(score)

	return plagiarism_results
