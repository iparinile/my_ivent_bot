import sqlite3
import db_comm

db = sqlite3.connect('mydata.sqlite')
cursor = db.cursor()

cursor.execute("""CREATE TABLE Users(
user_id INTEGER PRIMARY KEY,
name VARCHAR(30),
status INTEGER)""")

cursor.execute("""CREATE TABLE Events(
number_event INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name_event VARCHAR(30))""")

cursor.execute("""CREATE TABLE Main(
counter INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
user_id INTEGER ,
number_event INTEGER,
name_event VARCHAR(30),
status INTEGER)""")

db_comm.add_event('Круг сатаны', cursor, db)
db_comm.add_event('Судная ночь', cursor, db)
db_comm.add_event('Понедельник', cursor, db)

db.commit()
