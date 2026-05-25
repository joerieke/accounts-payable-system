import sqlite3

conn = sqlite3.connect("ap_system.db")
cursor = conn.cursor()

cursor.execute("""
SELECT vendor_id,
       vendor_code,
       vendor_name,
       vendor_address,
       vendor_phone,
       vendor_email
FROM vendors
ORDER BY vendor_id
""")

rows = cursor.fetchall()

print("\nVENDORS TABLE\n")

for r in rows:
    print(r)

conn.close()
