#!/usr/bin/env python3
# coding=utf-8

from mysql.connector import MySQLConnection, Error
from queries import auth_query, \
					create_user_query, \
					add_note_query, \
					get_all_notes_query, \
					get_note_by_id_query, \
					delete_note_by_id_query, \
					clear_notes_query


def connect(host='localhost', database=None, user=None, password=None):
	""" Connect to MySQL database """
	connected = None
	try:
		connected = MySQLConnection(password=password, user=user, host=host, database=database)

	finally:
		return connected


def disconnect(connection=None):
	try:
		if connection is not None:
			connection.close()
			return True
	except Error:
		return False


if __name__ == '__main__':
	conn = connect('localhost', 'notification_utils', 'nu_db_admin', '210jidojdxwq9223HAdas')
	user_id = auth_query(fullname='lalala', password='lalala', connection=conn)
	# if user_id is None:
	# 	response = create_user_query(fullname='lalala', password='lalala', connection=conn)
	# response = add_note_query(
	# 							user_id=user_id,
	# 							title='New note', 
	# 							text='Test note', 
								# files=['home/anton/Downloads/', 'home/anton'], 
								# tags=['study', 'work'],
	# 							connection=conn
	# 						)
	# response = get_all_notes_query(user_id=user_id, connection=conn)
	# response = get_note_by_id_query(user_id=user_id, note_id=17, connection=conn)
	# response = delete_note_by_id_query(user_id=user_id, note_id=16, connection=conn)
	response = clear_notes_query(user_id=user_id, connection=conn)	
	print(response)
	disconnect(conn)