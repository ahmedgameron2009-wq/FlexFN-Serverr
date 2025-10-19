import sqlite3, time

token = "zniQ8n8GeT6FAomr0v0O7RXK"  # el mismo que usa tu checker
now = int(time.time())
expires = now + 30 * 86400  # 30 días de validez

conn = sqlite3.connect("licenses.db")
c = conn.cursor()

# Crear la tabla si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS licenses (
    token TEXT PRIMARY KEY,
    created_at INTEGER,
    expires_at INTEGER,
    uses_allowed INTEGER DEFAULT 1,
    uses_count INTEGER DEFAULT 0,
    note TEXT DEFAULT ''
)
""")

# Insertar o reemplazar la licencia
c.execute("INSERT OR REPLACE INTO licenses (token, created_at, expires_at) VALUES (?, ?, ?)",
          (token, now, expires))

conn.commit()
conn.close()

print("✅ Licencia añadida correctamente:", token)