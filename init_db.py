import sqlite3

connection = sqlite3.connect('database.db')


with open('users.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()
