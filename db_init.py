import sqlite3

conn = sqlite3.connect("licenses.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS licenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT UNIQUE NOT NULL,
    created_at INTEGER,
    expires_at INTEGER,
    uses_allowed INTEGER,
    uses_count INTEGER,
    note TEXT,
    revoked INTEGER DEFAULT 0,
    first_ip TEXT
)
""")

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente (licenses.db)")
