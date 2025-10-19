License bot & server - README

Files:
- bot.py         : Discord bot to generate/revoke/list licenses (owner-only commands)
- server.py      : Flask server exposing /validate?token=...
- db_init.py     : Initialize SQLite DB (licenses.db)
- config.example.json : Template for bot config (put real values in config.json)
- requirements.txt : Python dependencies

Quick start (Linux/macOS/Windows PowerShell):
1. Create venv:
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Windows cmd:
   venv\Scripts\activate.bat
   # Linux/mac:
   source venv/bin/activate

2. Install deps:
   pip install -r requirements.txt

3. Initialize DB:
   python db_init.py

4. Create config.json from config.example.json and fill discord_token and admin_id.

5. Start server:
   python server.py

6. Start bot in another terminal:
   python bot.py

Usage (Discord, only admin_id can use commands):
- !genlicense <days> <uses> [note]  -> generate license token
- !revokelicense <token>           -> revoke
- !listlicenses                    -> list recent licenses

Security notes:
- Do not expose discord_token or admin_id publicly.
- Use HTTPS in production.
- Protect server endpoints if exposed to the internet.
