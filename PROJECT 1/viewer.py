import sqlite3
import os

# Open the same database file
db_path = os.path.abspath("qr_data.db")
print(f"📂 Reading from database: {db_path}\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM qr_entries")
rows = cursor.fetchall()

if rows:
    print("📊 Saved QR Entries:\n")
    print("{:<5} {:<50} {:<20}".format("ID", "QR Data", "Scan Time"))
    print("-" * 80)
    for row in rows:
        print("{:<5} {:<50} {:<20}".format(row[0], row[1][:48], row[2]))
else:
    print("⚠️ No entries found in the database.")

conn.close()
