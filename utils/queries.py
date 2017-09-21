import datetime
from mysql.connector import Error


def merge_note_with_files(notes=None):
	"""Merge notes with the same id"""
	if notes is  None:
		return None

	response = {}

	for note in notes:
		id = note[0]
		same_note = response.get(id)

		if same_note is not None:
			response[id][-1].append(note[-1])
		else:
			response[id] = list(note)
			file = response[id][-1] 
			response[id][-1] = []
			response[id][-1].append(file)

	response = list(response.values())
	return response


def auth_query(fullname=None, password=None, connection=None):
	cursor = None
	response = None

	if connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("SELECT user_id \
						FROM user \
						WHERE fullname='{fullname}' AND password='{password}' LIMIT 1"
						.format(fullname=fullname, password=password))

		response = cursor.fetchone()[0]

	finally:
		cursor.close()
		return response


def create_user_query(fullname=None, password=None, connection=None):
	cursor = None
	response = False

	if connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO user (fullname, password) VALUES ('{fullname}', '{password}')"
						.format(fullname=fullname, password=password))

		connection.commit()
		response = True

	finally:
		cursor.close()
		return response


def add_note_query(user_id=None, title=None, text=None, files=None, connection=None):
	cursor = None
	response = False

	if user_id is None or connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO note (title, text, modified_date, user_id) \
						VALUES ('{title}', '{text}', '{modified_date}', '{user_id}')"
						.format(title=title, 
								text=text, 
								modified_date=datetime.datetime.now(), 
								user_id=user_id
								)
						)

		connection.commit()
		add_files_query(files=files, note_id=cursor.lastrowid, connection=connection)

		response = True

	finally:
		cursor.close()
		return response	


def add_files_query(files=None, note_id=None, connection=None):
	if files is None or note_id is None or connection is None:
		return

	cursor = None

	try:
		cursor = connection.cursor()

		for file in files:
			cursor.execute("INSERT INTO file (path, note_id) \
							VALUES ('{path}', '{note_id}')"
							.format(path=file,
									note_id=note_id
									)
							)

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
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, f.path \
						FROM note n \
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						WHERE n.user_id='{user_id}'"
						.format(user_id=user_id))

		notes = cursor.fetchall()
		response = merge_note_with_files(notes)
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
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, f.path \
						FROM note n \
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						WHERE n.note_id='{note_id}' AND n.user_id='{user_id}'"
						.format(note_id=note_id, user_id=user_id))

		notes = cursor.fetchall()
		response = merge_note_with_files(notes)[0]

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
		cursor.execute("DELETE FROM note \
						WHERE note_id='{note_id}' AND user_id='{user_id}'"
						.format(note_id=note_id, user_id=user_id))

		connection.commit()
		response = True

	finally:
		cursor.close()
		return response



