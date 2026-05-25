import sqlite3

conn = sqlite3.connect("ap_system.db")
cursor = conn.cursor()

cursor.execute("""
SELECT invoice_id,
       vendor_id,
       vendor_invoice_number,
       payment_amount,
       vendor_payment_date,
       notes
FROM vendor_invoices
ORDER BY invoice_id
""")

rows = cursor.fetchall()

print("\nINVOICE TABLE\n")

for r in rows:
    print(r)

conn.close()
