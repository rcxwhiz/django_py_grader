import sqlite3

from old_code.server.dao import *


class NumberSubmissionsDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {number_submissions_table};
		CREATE TABLE {number_submissions_table} (
		{net_id_column} TEXT NOT NULL,
		{assignment_name_column} TEXT NOT NULL,
		{number_submissions_column} INTEGER NOT NULL);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()
