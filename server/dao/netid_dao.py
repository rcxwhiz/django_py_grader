import sqlite3

from server.dao import *


class NetIdDao:
	def __init__(self):
		self.conn = sqlite3.connect(database_path)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def reset_table(self):
		sql_cmd = f"""
		DROP TABLE IF EXISTS {net_ids_table};
		CREATE TABLE {net_ids_table} (
		{net_id_column} TEXT NOT NULL PRIMARY KEY);
		"""
		self.cursor.executescript(sql_cmd)
		self.conn.commit()
