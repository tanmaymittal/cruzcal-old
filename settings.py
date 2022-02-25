"""
Helper function that connects to MySQLdb
"""
import pymysql as MySQLdb

database_host = 'sql3.freemysqlhosting.net '
database_user = 'sql3475197'
database_password = '1pge27alQw'
database_name = 'sql3475197'


def connection():
	conn = MySQLdb.connect(host=database_host, user = database_user, passwd = database_password, db = database_name)
	c = conn.cursor()
	return c, conn