#!/usr/bin/env python3
# coding=utf-8

import datetime
# from mysql.connector import Error
import cx_Oracle


def _merge_note_with_files(notes=None):
	"""Merge notes with the same id"""
	if notes is  None:
		return None

	response = []
	duplicated = {}

	for note in notes:
		note_id = note[0]
		same_note = duplicated.get(note_id)

		if same_note is None:
			duplicated[note_id] = list(note)
		else:
			for i, field in enumerate(note):
				if isinstance(duplicated[note_id][i], list):
					if field not in duplicated[note_id][i] and field is not None:
						duplicated[note_id][i].append(field)
				elif field != duplicated[note_id][i] and field is not None:
					tmp = duplicated[note_id][i]
					duplicated[note_id][i] = []
					duplicated[note_id][i].append(tmp)
					duplicated[note_id][i].append(field)

	response = list(duplicated.values())

	return response

def auth_query(fullname=None, password=None, connection=None):
	cursor = None
	response = None

	if connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callfunc('auth', int, (fullname, password))

	finally:
		cursor.close()
		return response


def create_user_query(fullname=None, password=None, connection=None):
	cursor = None
	response = None

	if connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callfunc('create_user', int, (fullname, password))
		connection.commit()
	finally:
		cursor.close()
		return response


def add_note_query(user_id=None, title=None, text=None, files=None, tags=None, connection=None):
	cursor = None
	response = False

	if user_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callproc('create_note', (title, text, datetime.datetime.now(), user_id))

		connection.commit()
		_add_files_query(files=files, note_id=cursor.lastrowid, connection=connection)
		_add_tag_note_query(tags=tags, note_id=cursor.lastrowid, connection=connection)
		response = True

	finally:
		cursor.close()
		return response	


def _add_tag_note_query(tags=None, note_id=None, connection=None):
	if tags is None or note_id is None or connection is None:
		return

	cursor = None

	try:
		tags_id = _get_or_create_tags_query(tags, connection)
		cursor = connection.cursor()

		for tag_id in tags_id:
			response = cursor.callproc('create_tag_note', (tag_id, note_id))

		connection.commit()

	finally:
		cursor.close()


def _get_or_create_tags_query(tags=None, connection=None):
	cursor = None
	response = []

	if tags is None or connection is None:
		return response

	try:
		cursor = connection.cursor()

		for tag in tags:

			try:
				tag_response = cursor.callfunc('get_tag_by_title', int, (tag))
				response.append(tag_response)
			except Exception:
				tag_id = _create_tag_query(tag, connection)

				if tag_id is not None:
					response.append(tag_id)
	finally:
		cursor.close()
		return response


def _create_tag_query(tag=None, connection=None):
	cursor = None
	response = None

	if tag is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callfunc('create_tag', int, (tag,))
		connection.commit()

	finally:
		cursor.close()
		return response


def _add_files_query(files=None, note_id=None, connection=None):
	if files is None or note_id is None or connection is None:
		return

	cursor = None

	try:
		cursor = connection.cursor()

		for file in files:
			response = cursor.callproc('create_attach', (file, note_id))

		connection.commit()

	finally:
		cursor.close()

def get_all_notes_query(user_id=None, connection=None):
	cursor = None
	response = None

	if user_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
				FROM note n \
				LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
				LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
				LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
				WHERE n.account_id='{user_id}'"
				.format(user_id=user_id))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)

	finally:
		cursor.close()
		return response


def get_note_by_id_query(user_id=None, note_id=None, connection=None):
	cursor = None
	response = None

	if user_id is None or note_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
						WHERE n.note_id='{note_id}' AND n.account_id='{user_id}'"
						.format(note_id=note_id, user_id=user_id))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)[0]

	finally:
		cursor.close()
		return response


def delete_note_by_id_query(user_id=None, note_id=None, connection=None):
	cursor = None
	response = False

	if user_id is None or note_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callproc('delete_note', (user_id, note_id))

		connection.commit()
		response = True

	finally:
		cursor.close()
		return response


def find_notes_by_title_query(user_id=None, title=None, connection=None):
	cursor = None
	response = None

	if user_id is None or title is None  or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
						WHERE n.account_id='{user_id}' AND n.title='{title}'"
						.format(user_id=user_id, title=title))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)

	finally:
		cursor.close()
		return response	


def find_notes_by_text_query(user_id=None, text=None, connection=None):
	cursor = None
	response = None

	if user_id is None or text is None  or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
						WHERE n.account_id='{user_id}' AND n.text LIKE '%{text}%'"
						.format(user_id=user_id, text=text))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)

	finally:
		cursor.close()
		return response	


def find_notes_by_date_query(user_id=None, date=None, connection=None):
	cursor = None
	response = None

	if user_id is None or date is None  or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
						WHERE n.account_id='{user_id}' \
						AND DAY(n.modified_date)=DAY('{date}') \
						AND MONTH(n.modified_date)=MONTH('{date}') \
						AND YEAR(n.modified_date)=YEAR('{date}')"
						.format(user_id=user_id, date=date))

		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
				FROM note n \
				LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
				LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
				LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
				WHERE n.account_id='{user_id}' \
				AND to_date(n.modified_date, 'DD-MM-YY') = to_date('{date}', 'DD-MM-YY')"
				.format(user_id=user_id, date=date.strftime('%d-%m-%Y')))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)
	finally:
		cursor.close()
		return response	


def find_notes_by_tag_query(user_id=None, tag=None, connection=None):
	cursor = None
	response = None

	if user_id is None or tag is None  or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN attach f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_link=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_link=t.tag_id \
						WHERE n.account_id='{user_id}' \
						AND t.title='{tag}'"
						.format(user_id=user_id, tag=tag))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)
	except Exception as e:
		print(e)

	finally:
		cursor.close()
		return response	


def update_note_by_id_query(user_id=None, 
							note_id=None, 
							title=None, 
							text=None, 
							files=None, 
							tags=None, 
							connection=None):
	cursor = None
	response = False

	if user_id is None or note_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()

		note = get_note_by_id_query(user_id=user_id, note_id=note_id, connection=connection)

		if note is None:
			return response

		response = cursor.callproc('update_note', (title, text, datetime.datetime.now(), note_id, user_id))
		connection.commit()
		_add_files_query(files=files, note_id=note_id, connection=connection)
		_add_tag_note_query(tags=tags, note_id=note_id, connection=connection)
		response = True

	finally:
		cursor.close()
		return response


def clear_notes_query(user_id=None, connection=None):
	cursor = None
	response = False

	if user_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		response = cursor.callproc('clear_notes', (user_id,))
		connection.commit()
		response = True

	finally:
		cursor.close()
		return response



