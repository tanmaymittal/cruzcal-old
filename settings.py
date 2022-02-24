"""
Helper function that connects to MySQLdb
"""
import MySQLdb

database_host = 'localhost'
database_user = 'root'
database_password = ''
database_name = ''


def connection():
	conn = MySQLdb.connect(host=database_host, user = database_user, passwd = database_password, db = database_name)
	c = conn.cursor()
	return c, conn