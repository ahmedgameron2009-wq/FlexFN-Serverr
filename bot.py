import discord
from discord.ext import commands
import sqlite3
import time
import secrets
import json
from pathlib import Path

CFG_PATH = "config.json"
if not Path(CFG_PATH).exists():
    raise SystemExit("Create config.json from config.example.json")

with open(CFG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

TOKEN = cfg.get("discord_token")
ADMIN_ID = int(cfg.get("admin_id"))
DB_PATH = cfg.get("db_path", "licenses.db")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def gen_token(nbytes=18):
    return secrets.token_urlsafe(nbytes)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} (Owner ID: {ADMIN_ID})")

def admin_only():
    async def predicate(ctx):
        return ctx.author.id == ADMIN_ID
    return commands.check(predicate)

@bot.command()
@admin_only()
async def genlicense(ctx, days: int, uses: int = 1, *, note: str = ""):
    token = gen_token()
    now = int(time.time())
    expires = now + days * 86400 if days > 0 else None
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO licenses (token, created_at, expires_at, uses_allowed, uses_count, note, revoked, first_ip)
        VALUES (?, ?, ?, ?, 0, ?, 0, '')
    """, (token, now, expires, uses, note))
    conn.commit()
    conn.close()
    await ctx.send(f"✅ License generated:\n`{token}`\nExpires in {days} days. Uses allowed: {uses}\nNote: \"{note}\"")

if __name__ == "__main__":
    bot.run(TOKEN)
