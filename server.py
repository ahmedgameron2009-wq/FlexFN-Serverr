from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Ruta principal (solo para probar)
@app.route('/')
def home():
    return jsonify({"status": "online", "message": "FlexFN Server is running!"})

# Ruta de validación de licencia
@app.route('/validate', methods=['GET'])
def validate():
    token = request.args.get('token')
    if not token:
        return jsonify({"valid": False, "error": "Token not provided"})

    db_path = os.path.join(os.path.dirname(__file__), "licenses.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT key, expire_date FROM licenses WHERE key=?", (token,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"valid": False, "error": "Invalid license"})

    # Verificar expiración
    import datetime
    expire_date = datetime.datetime.strptime(row[1], "%Y-%m-%d")
    remaining_days = (expire_date - datetime.datetime.now()).days

    if remaining_days <= 0:
        return jsonify({"valid": False, "error": "License expired"})
    else:
        return jsonify({"valid": True, "days_left": remaining_days})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
