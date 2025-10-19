from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

DB_PATH = "licenses.db"
app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/validate", methods=["GET", "POST"])
@app.route("/validate/validate", methods=["GET", "POST"])  # <-- acepta ambas rutas
def validate():
    # Soporte para GET y POST
    token = None
    if request.method == "GET":
        token = request.args.get("token", "").strip()
    elif request.is_json:
        data = request.get_json(force=True)
        token = data.get("key", "").strip() if data else ""

    if not token:
        return jsonify({"valid": False, "reason": "missing_token"}), 400

    client_ip = request.remote_addr or request.environ.get("HTTP_X_FORWARDED_FOR", "")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM licenses WHERE token = ?", (token,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({"valid": False, "reason": "not_found"}), 200
    if row["revoked"]:
        return jsonify({"valid": False, "reason": "revoked"}), 200

    return jsonify({
        "valid": True,
        "reason": "ok",
        "expires_at": row["expires_at"],
        "first_ip": row["first_ip"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
