import sqlite3

db = sqlite3.connect('mydata.sqlite')
cursor = db.cursor()

cursor.execute("""CREATE TABLE Users(
counter INT PRIMARY KEY, 
user_id INTEGER NOT NULL,
name VARCHAR(30))""")

cursor.execute("""CREATE TABLE Events(
counter INT PRIMARY KEY,
name_event VARCHAR(30))""")

cursor.execute("""CREATE TABLE Communication(
user_id INTEGER NOT NULL,
name_event VARCHAR(30) ,
status INTEGER )""")

db.commit()
