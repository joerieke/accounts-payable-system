import sqlite3

conn = sqlite3.connect("ap_system.db")
cursor = conn.cursor()

cursor.execute("""
SELECT SUM(payment_amount)
FROM vendor_invoices
""")

cursor.execute("""
SELECT COUNT(invoice_id)
FROM vendor_invoices
""")

cursor.execute("""
SELECT vendor_id,
       COUNT(invoice_id),
       SUM(payment_amount)
FROM vendor_invoices
GROUP BY vendor_id
ORDER BY SUM(payment_amount) DESC
""")

cursor.execute("""
SELECT v.vendor_code,
       COUNT(i.invoice_id),
       SUM(i.payment_amount)
FROM vendor_invoices i
JOIN vendors v ON i.vendor_id = v.vendor_id
GROUP BY v.vendor_code
ORDER BY SUM(i.payment_amount) DESC
""")

cursor.execute("""
SELECT invoice_id,
       vendor_id,
       payment_amount
FROM vendor_invoices
ORDER BY payment_amount DESC
LIMIT 1
""")

rows = cursor.fetchall()

print("\nINVOICE TABLE\n")

for r in rows:
    print(r)

conn.close()
