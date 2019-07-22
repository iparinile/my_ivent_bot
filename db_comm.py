def get_event_list(cursor):
    cursor.execute(f"SELECT * FROM Events")
    # print(cursor.fetchall())
    return cursor.fetchall()


def number_events(cursor):
    cursor.execute(f"SELECT COUNT (number) FROM Events")
    return cursor.fetchall()


def insert_consent(user_id, number_event, cursor, db):
    cursor.execute(f"INSERT INTO Communication (user_id, name_event, status) VALUES ({user_id}, {number_event}, 0)")
    db.commit()


def add_user(counter, user_id, name, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (counter, user_id, name) VALUES ({counter}, {user_id}, {name}")
    db.commit()


def get_name_event(number, cursor):
    cursor.execute(f"SELECT name_event FROM Events WHERE number={number} ")
    return str(cursor.fetchall())[2:-3]


def add_event(name_event, cursor, db):
    cursor.execute(f"INSERT INTO Events (name_event) VALUES ('{name_event}')")
    db.commit()
