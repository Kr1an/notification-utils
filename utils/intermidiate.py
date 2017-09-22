from utils.connector import connect, disconnect
from utils.queries import \
    auth_query, \
    create_user_query, \
    add_note_query, \
    get_all_notes_query, \
    get_note_by_id_query, \
    delete_note_by_id_query, \
    clear_notes_query,  \
    find_notes_by_title_query, \
    find_notes_by_text_query, \
    find_notes_by_date_query, \
    find_notes_by_tag_query, \
    update_note_by_id_query


def authorized(func):
    def wrapper(options, connection={}):
        auth = options.get('auth')
        if not auth:
            raise Exception("NotAuthorized")
        user_id = _auth_command(auth.get('fullname'), auth.get('password'), connection)

        if not user_id:
            raise Exception("NotAuthorized")
        func.__globals__['user_id'] = user_id

        return func(options, connection)
    return wrapper


def _create_user_command(fullname=None, password=None, connection=None):
    return create_user_query(fullname, password, connection)


def _add_note_command(user_id=None, title=None, text=None, files=None, tags=None, connection=None):
    return add_note_query(user_id, title, text, files, tags, connection)


def _update_note_by_id_command(user_id=None, note_id=None, title=None, text=None, files=None, tags=None, connection=None):
    print()
    return update_note_by_id_query(user_id, note_id, title, text, files, tags, connection)


def _get_all_notes_command(user_id=None, connection=None):
    return get_all_notes_query(user_id, connection)


def _get_note_by_id_command(user_id=None, note_id=None, connection=None):
    return get_note_by_id_query(user_id, note_id, connection)


def _delete_note_by_id_command(user_id=None, note_id=None, connection=None):
    return delete_note_by_id_query(user_id, note_id, connection)


def _clear_notes_command(user_id=None, connection=None):
    return clear_notes_query(user_id, connection)


def _auth_command(fullname=None, password=None, connection=None):
    return auth_query(fullname=fullname, password=password, connection=connection)


def _find_notes_by_title_command(user_id=None, title=None, connection=None):
    return find_notes_by_title_query(user_id, title, connection)


def _find_notes_by_text_command(user_id=None, text=None, connection=None):
    return find_notes_by_text_query(user_id, text, connection)


def _find_notes_by_date_command(user_id=None, date=None, connection=None):
    return find_notes_by_date_query(user_id, date, connection)


def _find_notes_by_tag_command(user_id=None, tag=None, connection=None):
    return find_notes_by_tag_query(user_id, tag, connection)


def create_user(options, connection={}):
    auth = options.get('auth')
    return _create_user_command(auth.get('fullname'), auth.get('password'), connection)


@authorized
def delete(options, connection={}):
    args = options['args']
    if 'delete_by_id' in args:
        return _delete_note_by_id_command(user_id, args.get('delete_by_id'), connection)

    if 'delete_all' in args:
        return _clear_notes_command(user_id, connection)


@authorized
def update(options, connection={}):
    args = options['args']
    return _update_note_by_id_command(
        user_id,
        args.get('update_by_id'),
        args.get('update_with_title'),
        args.get('update_with_text'),
        args.get('update_with_files'),
        args.get('update_with_tags'),
        connection,


    )


@authorized
def find(options, connection={}):
    args = options['args']
    if 'find_by_title' in args:
        return _find_notes_by_title_command(user_id, args.get('find_by_title'), connection)

    if 'find_by_text' in args:
        return _find_notes_by_text_command(user_id, args.get('find_by_text'), connection)

    if 'find_by_date' in args:
        return _find_notes_by_date_command(user_id, args.get('find_by_date'), connection)

    if 'find_by_tag' in args:
        return _find_notes_by_tag_command(user_id, args.get('find_by_tag'), connection)


@authorized
def get(options, connection={}):
    args = options.get('args')
    if 'get_by_id' in args:
        return get_note_by_id_query(user_id, args.get('find_by_id'), connection)

    if 'get_all' in args:
        return _get_all_notes_command(user_id, connection)


@authorized
def add(options, connection={}):
    args = options.get('args')
    return _add_note_command(
        user_id,
        args.get('add_with_title'),
        args.get('add_with_text'),
        args.get('add_with_files'),
        args.get('add_with_tags'),
        connection
    )


method_chooser = {
    "create_user": create_user,
    "delete": delete,
    "update": update,
    "find": find,
    "get": get,
    "add": add,
}


def resolve_input(options):
    response = None
    connection = connect('localhost', 'notification_utils', 'nu_db_admin', '210jidojdxwq9223HAdas')
    try:
        response = method_chooser[options['method_type']](options, connection)

    except Exception as e:
        response = str(e);
    finally:
        disconnect(connection)
        return response

