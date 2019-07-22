import sqlite3
import db_comm

db = sqlite3.connect('mydata.sqlite')
cursor = db.cursor()

cursor.execute("""CREATE TABLE Users(
counter INT PRIMARY KEY, 
user_id INTEGER NOT NULL,
name VARCHAR(30))""")

cursor.execute("""CREATE TABLE Events(
number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name_event VARCHAR(30))""")

cursor.execute("""CREATE TABLE Communication(
user_id INTEGER NOT NULL,
number_event INTEGER,
status INTEGER)""")

db_comm.add_event('Круг сатаны', cursor, db)
db_comm.add_event('Судная ночь', cursor, db)
db_comm.add_event('Понедельник', cursor, db)

db.commit()
