def get_event_list(cursor):
    cursor.execute(f"SELECT * FROM Events")
    return cursor.fetchall()


def number_events(cursor):
    cursor.execute(f"SELECT COUNT (number) FROM Events")
    return cursor.fetchall()


def insert_consent(user_id, number_event, cursor, db):
    cursor.execute(f"UPDATE Users SET number_event={number_event} WHERE user_id={user_id}")
    db.commit()


def add_user(user_id, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (user_id) VALUES ({user_id})")
    db.commit()


def get_name_event(number, cursor):
    cursor.execute(f"SELECT name_event FROM Events WHERE number={number} ")
    return str(cursor.fetchall())[2:-3]


def get_name_event_from_user(user_id, cursor):
    cursor.execute(f"SELECT name_event FROM Users WHERE user_id={user_id}")
    return str(cursor.fetchall())[2:-3]


def add_event(name_event, cursor, db):
    cursor.execute(f"INSERT INTO Events (name_event) VALUES ('{name_event}')")
    db.commit()


def insert_name_event(number_event, cursor, db):
    cursor.execute(
        f"UPDATE Users SET name_event=(SELECT name_event FROM Events WHERE number_event = '{number_event}') "
        f"WHERE number_event='{number_event}'")
    db.commit()


def get_state(user_id, cursor):
    cursor.execute('SELECT status FROM Users WHERE user_id=' +
                   str(user_id))
    a = cursor.fetchall()
    if a is None or 0:
        return 0
    else:
        return a[0][0]


def set_state(user_id, status, cursor, db):
    cursor.execute('UPDATE Users SET status=' + str(status) +
                   ' WHERE user_id=' + str(user_id))
    db.commit()


def insert_name_of_user(user_id, name, cursore, db):
    cursore.execute(f"UPDATE Users SET name='{name}'  WHERE user_id={user_id}")
    db.commit()
