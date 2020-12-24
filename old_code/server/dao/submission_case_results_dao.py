import sqlite3

from old_code.server.dao import *


class SubmissionCaseResultsDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {submission_case_results_table};
		CREATE TABLE {submission_case_results_table} (
		{net_id_column} TEXT NOT NULL,
		{assignment_name_column} TEXT NOT NULL,
		{test_case_number_column} INTEGER NOT NULL,
		{submission_output_column} TEXT NOT NULL,
		{correct_column} INTEGER NOT NULL);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()
