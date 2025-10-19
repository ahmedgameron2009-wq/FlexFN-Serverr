from flask import Flask, request, jsonify
import sqlite3
import os
import datetime

app = Flask(__name__)

DB_NAME = "licenses.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def row_to_dict(row, cursor):
    return {cursor.description[i][0]: row[i] for i in range(len(row))}

@app.route("/")
def home():
    return jsonify({"status": "online", "message": "FlexFN Server is running!"})

@app.route("/validate", methods=["GET"])
def validate():
    token = request.args.get("token")
    if not token:
        return jsonify({"valid": False, "error": "Token not provided"}), 400

    if not os.path.exists(DB_PATH):
        return jsonify({"valid": False, "error": "Database not found"}), 500

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # ⚠️ Usamos el esquema del BOT: token + expires_at (epoch/segundos) + uses_allowed/uses_count opcional
        cur.execute("SELECT token, expires_at FROM licenses WHERE token=?", (token,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return jsonify({"valid": False, "error": "Invalid license"}), 404

        _token, expires_at = row

        # Licencia sin expiración (None o 0) => válida
        if expires_at is None or int(expires_at) == 0:
            return jsonify({"valid": True, "days_left": "Unlimited"}), 200

        # expires_at viene como timestamp (segundos)
        expire_dt = datetime.datetime.fromtimestamp(int(expires_at))
        days_left = (expire_dt - datetime.datetime.now()).days

        if days_left <= 0:
            return jsonify({"valid": False, "error": "License expired", "days_left": 0}), 403

        return jsonify({"valid": True, "days_left": days_left}), 200

    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
