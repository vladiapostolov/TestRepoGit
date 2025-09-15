import os
import sqlite3
from pathlib import Path
from typing import Iterator

# Use DB_PATH env var when set (e.g. in container we'll default to /data/app.db).
DB_PATH = Path(os.environ.get("DB_PATH", "/data/app.db"))


def init_db() -> None:
    """Create database file and tables if they don't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    """Return a new sqlite3.Connection using the DB_PATH."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def iter_items() -> Iterator[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM items ORDER BY id")
        for row in cur.fetchall():
            yield {"id": row[0], "name": row[1]}
    finally:
        conn.close()


def add_item(name: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name) VALUES (?)", (name,))
        conn.commit()
        item_id = cur.lastrowid
        return {"id": item_id, "name": name}
    finally:
        conn.close()
