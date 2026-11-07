import sqlite3
import json

conn = sqlite3.connect('data/omniverse.db')
cur = conn.cursor()

print('--- TABLES ---')
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables count:", len(tables))
print("Tables:", tables)

if "client_audit_records" in tables:
    print('\n--- CLIENT AUDIT RECORDS ---')
    cur.execute('SELECT COUNT(*), COUNT(DISTINCT hub), COUNT(DISTINCT sector), COUNT(DISTINCT client_name) FROM client_audit_records')
    res = cur.fetchone()
    print('Count, distinct hubs, distinct sectors, distinct clients:', res)

    cur.execute('SELECT DISTINCT hub FROM client_audit_records ORDER BY hub')
    print('Hubs:', [r[0] for r in cur.fetchall()])

    cur.execute('SELECT DISTINCT sector FROM client_audit_records ORDER BY sector')
    print('Sectors:', [r[0] for r in cur.fetchall()])

    cur.execute('SELECT client_name, hub, sector, performance_score, seo_score, conversion_score, overall_health, estimated_monthly_loss_usd FROM client_audit_records LIMIT 5')
    for row in cur.fetchall():
        print("Sample client audit:", row)

if "security_audit_records" in tables:
    print('\n--- SECURITY AUDIT RECORDS ---')
    cur.execute('SELECT COUNT(*), COUNT(DISTINCT action_type) FROM security_audit_records')
    print('Count, distinct actions:', cur.fetchone())

    cur.execute('SELECT action_type, status, approver, details_json FROM security_audit_records LIMIT 3')
    for row in cur.fetchall():
        print("Sample sec record:", row)
