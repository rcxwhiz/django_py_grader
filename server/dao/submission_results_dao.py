import sqlite3

from server.dao import *


class SubmissionResultsDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {submission_results_table};
		CREATE TABLE {submission_results_table} (
		{net_id_column} TEXT NOT NULL,
		{assignment_name_column} TEXT NOT NULL,
		{submission_code_column} TEXT NOT NULL,
		{submission_time_column} INTEGER NOT NULL,
		{submission_number_column} INTEGER NOT NULL,
		{submission_grade_column} REAL NOT NULL);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()
