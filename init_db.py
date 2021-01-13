import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('Milox zwolniony z pewnej firmy', 'Milox zwolniony z pewnej firmy')
                )
    connection.commit()
    connection.close()
