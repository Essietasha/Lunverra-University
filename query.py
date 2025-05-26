import sqlite3
import os

db_path = os.path.join("instance", "ludb.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Fetch all users
cursor.execute("SELECT * FROM User;")
userRows = cursor.fetchall()
for user in userRows:
    print(user)

conn.close()
