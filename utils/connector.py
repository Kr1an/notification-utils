#!/usr/bin/env python3
# coding=utf-8

from mysql.connector import MySQLConnection, Error


def connect(host='localhost', database=None, user=None, password=None):
	""" Connect to MySQL database """
	connection = None
	try:
		connection = MySQLConnection(password=password, user=user, host=host, database=database)

	finally:
		return connection


def disconnect(connection=None):
	try:
		if connection is not None:
			connection.close()
			return True
	except Error:
		return False


if __name__ == '__main__':
	pass
	# from queries import auth_query, \
	# 				create_user_query, \
	# 				add_note_query, \
	# 				get_all_notes_query, \
	# 				get_note_by_id_query, \
	# 				delete_note_by_id_query, \
	# 				clear_notes_query, \
	# 				find_notes_by_title_query, \
	# 				find_notes_by_text_query, \
	# 				find_notes_by_date_query, \
	# 				find_notes_by_tag_query, \
	# 				update_note_by_id_query


	# conn = connect('localhost', 'notification_utils', 'nu_db_admin', '210jidojdxwq9223HAdas')
	# user_id = auth_query(fullname='lalala', password='lalala', connection=conn)
	# if user_id is None:
	# 	response = create_user_query(fullname='lalala', password='lalala', connection=conn)
	# response = add_note_query(
	# 							user_id=user_id,
	# 							title='Find me', 
	# 							text='Test note', 
	# 							files=['home/anton/Downloads/', 'home/anton'], 
	# 							tags=['study', 'work'],
	# 							connection=conn
	# 						)
	# response = get_all_notes_query(user_id=user_id, connection=conn)
	# response = get_note_by_id_query(user_id=user_id, note_id=17, connection=conn)
	# response = delete_note_by_id_query(user_id=user_id, note_id=16, connection=conn)
	# response = clear_notes_query(user_id=user_id, connection=conn)
	# response = find_notes_by_title_query(user_id=user_id, title='Find me', connection=conn)	
	# response = find_notes_by_text_query(user_id=user_id, text='Test note', connection=conn)	
	# response = find_notes_by_date_query(user_id=user_id, date='2017-09-22', connection=conn)
	# response = find_notes_by_tag_query(user_id=user_id, tag='study', connection=conn)	
	# response = update_note_by_id_query(
	# 							user_id=user_id,
	# 							note_id=19,
	# 							title='Lalala', 
	# 							text='Test note', 
	# 							files=['home/anton/Downloads/', 'home/anton'], 
	# 							tags=['study', 'kekeke'],
	# 							connection=conn
	# 						)
	# print(response)
	disconnect(conn)