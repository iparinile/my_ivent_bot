def get_event_list(cursor):
    cursor.execute(f"SELECT * FROM Events")
    return cursor.fetchall()


def number_events(cursor):
    cursor.execute(f"SELECT COUNT (number) FROM Events")
    return cursor.fetchall()


def insert_consent(user_id, number_event, cursor, db):
    cursor.execute(f"UPDATE OR IGNORE Main SET number_event={number_event}, user_id={user_id}")
    cursor.execute(f"INSERT OR IGNORE INTO Main (number_event, user_id) VALUES ({number_event}, {user_id})")
    db.commit()


def add_user(user_id, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (user_id) VALUES ({user_id})")
    db.commit()


def get_name_event(number_event, cursor):
    cursor.execute(f"SELECT name_event FROM Events WHERE number_event={number_event} ")
    return str(cursor.fetchall())[2:-3]


def get_name_event_from_user(user_id, cursor):
    cursor.execute(f"SELECT name_event FROM Users WHERE user_id={user_id}")
    return str(cursor.fetchall())[2:-3]


def add_event(name_event, cursor, db):
    cursor.execute(f"INSERT INTO Events (name_event) VALUES ('{name_event}')")
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


def set_state_main(user_id, status, cursor, db):
    cursor.execute('UPDATE Main SET status=' + str(status) +
                   ' WHERE user_id=' + str(user_id))
    db.commit()


def add_user_to_main(user_id, number_event, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Main (user_id, number_event ,name_event , status) VALUES ({user_id}, "
                   f"{number_event}, {get_name_event(number_event, cursor)}, 1)")
    db.commit()


def something(user_id, number_event, cursor):
    cursor.execute(f"SELECT counter FROM Main WHERE user_id={user_id} AND number_event={number_event}")
    return cursor.fetchone()


def get_state_from_main(user_id, cursor):
    cursor.execute('SELECT status FROM Main WHERE user_id=' +
                   str(user_id))
    a = cursor.fetchall()
    if not a:
        return 0
    else:
        for i in range(len(a)):
            if a[i][0] == 1:
                return a[i][0]


def get_event_list_from_main(user_id, cursor):
    cursor.execute(
        f"SELECT name_event, number_event FROM Main WHERE user_id={user_id} AND status={get_state_from_main(user_id, cursor)}")
    return cursor.fetchall()


def check_in(user_id, number_event, cursor, db):
    cursor.execute(f"UPDATE Main SET status=2 WHERE user_id={user_id} AND number_event={number_event}")
    db.commit()


def statistics(cursor):
    cursor.execute(f"SELECT name_event FROM Main WHERE status=1")
    print(cursor.fetchall())


def get_event_to_statistics(number_event, cursor):
    cursor.execute(f"SELECT status FROM Main WHERE number_event={number_event}")
    return cursor.fetchall()