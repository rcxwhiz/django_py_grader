import sqlite3

from old_code.server.dao import *


class AssignmentsDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {assignments_table};
		CREATE TABLE {assignments_table} (
		{assignment_name_column} TEXT NOT NULL PRIMARY KEY,
		{assignment_key_code_column} TEXT NOT NULL,
		{assignment_open_time_column} INTEGER NOT NULL,
		{assignment_close_time_column} INTEGER NOT NULL,
		{total_submissions_column} INTEGER NOT NULL,
		{total_unique_submissions_column} INTEGER NOT NULL,
		{number_allowed_submissions_column} INTEGER NOT NULL,
		{number_test_cases_column} INTEGER NOT NULL,
		{grading_method_column} INTEGER NOT NULL);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()
