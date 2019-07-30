import sqlite3
import db_comm

db = sqlite3.connect('mydata.sqlite')
cursor = db.cursor()

cursor.execute('CREATE TABLE Users(\n'
               'user_id INTEGER PRIMARY KEY,\n'
               'name VARCHAR(30),\n'
               'status INTEGER)')

cursor.execute("CREATE TABLE Events(\n"
               "number_event INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n"
               "name_event VARCHAR(30))")

cursor.execute("CREATE TABLE Main(\n"
               "counter INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n"
               "user_id INTEGER ,\n"
               "number_event INTEGER,\n"
               "name_event VARCHAR(30),\n"
               "status INTEGER)")

db_comm.add_event('Круг сатаны', cursor, db)
db_comm.add_event('Судная ночь', cursor, db)
db_comm.add_event('Понедельник', cursor, db)

db.commit()
