

import sqlite3

conn = sqlite3.connect("tennis_db.sqlite")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(Competitor_Rankings);")
print(cursor.fetchall())
conn.close()
