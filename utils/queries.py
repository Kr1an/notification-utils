import datetime
from mysql.connector import Error


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
	response = None

	if connection is None:
		return response

	try:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO user (fullname, password) VALUES ('{fullname}', '{password}')"
						.format(fullname=fullname, password=password))

		connection.commit()
		response = cursor.lastrowid

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
		cursor.execute("INSERT INTO note (title, text, modified_date, user_id) \
						VALUES ('{title}', '{text}', '{modified_date}', '{user_id}')"
						.format(title=title, 
								text=text, 
								modified_date=datetime.datetime.now(), 
								user_id=user_id
								)
						)

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
			cursor.execute("INSERT INTO tag_note (note_id, tag_id) \
							VALUES ('{note_id}', '{tag_id}')"
							.format(note_id=note_id,
									tag_id=tag_id
									)
							)

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
			cursor.execute("SELECT tag_id \
							FROM tag \
							WHERE title='{tag}' LIMIT 1"
							.format(tag=tag))

			tag_response = cursor.fetchone()
			if tag_response is not None:
				response.append(tag_response[0])
			else:
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
		cursor.execute("INSERT INTO tag (title) VALUES ('{title}')"
						.format(title=tag))

		response = cursor.lastrowid
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
		cursor.execute("SELECT n.note_id, n.title, n.text, n.modified_date, t.title, f.path\
						FROM note n \
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.user_id='{user_id}'"
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
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.note_id='{note_id}' AND n.user_id='{user_id}'"
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
		cursor.execute("DELETE FROM note \
						WHERE note_id='{note_id}' AND user_id='{user_id}'"
						.format(note_id=note_id, user_id=user_id))

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
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.user_id='{user_id}' AND n.title='{title}'"
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
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.user_id='{user_id}' AND n.text LIKE '%{text}%'"
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
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.user_id='{user_id}' \
						AND DAY(n.modified_date)=DAY('{date}') \
						AND MONTH(n.modified_date)=MONTH('{date}') \
						AND YEAR(n.modified_date)=YEAR('{date}')"
						.format(user_id=user_id, date=date))

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
						LEFT OUTER JOIN file f ON f.note_id=n.note_id \
						LEFT OUTER JOIN tag_note tn ON tn.note_id=n.note_id \
						LEFT OUTER JOIN tag t ON tn.tag_id=t.tag_id \
						WHERE n.user_id='{user_id}' \
						AND t.title='{tag}'"
						.format(user_id=user_id, tag=tag))

		notes = cursor.fetchall()
		response = _merge_note_with_files(notes)
	except Error as e:
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

		cursor.execute("UPDATE note \
						SET title='{title}', text='{text}', modified_date='{modified_date}' \
						WHERE note_id='{note_id}' AND user_id='{user_id}'"
						.format(title=title, 
								text=text, 
								modified_date=datetime.datetime.now(), 
								user_id=user_id,
								note_id=note_id
								)
						)

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
		cursor.execute("DELETE FROM note \
						WHERE user_id='{user_id}'"
						.format(user_id=user_id))

		connection.commit()
		response = True

	finally:
		cursor.close()
		return response



