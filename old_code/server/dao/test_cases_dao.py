import sqlite3

from old_code.server.dao import *


class TestCasesDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {test_case_table};
		CREATE TABLE {test_case_table} (
		{assignment_name_column} TEXT NOT NULL,
		{test_case_number_column} INTEGER NOT NULL,
		{test_case_input_column} TEXT NOT NULL,
		{test_case_output_column} TEXT NOT NULL);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()

	def add_test_case(self, assignment_name: str, test_text: str) -> bool:
		pass
