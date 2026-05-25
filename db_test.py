import sqlite3

conn = sqlite3.connect("ap_system.db")
cursor = conn.cursor()

cursor.execute("SELECT vendor_id, vendor_code, vendor_name FROM vendors")
print(cursor.fetchall())

##for r in rows:
##    print(r)

conn.close()
