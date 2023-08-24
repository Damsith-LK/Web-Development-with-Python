# Day 63 - Learning about SQL
# I will have to download DB browser from https://sqlitebrowser.org/dl/

import sqlite3

# Creating a connection to a new database
db = sqlite3.connect("books-database.db")

# Creating a cursor which will control our database
cursor = db.cursor()
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")