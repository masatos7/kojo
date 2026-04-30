import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "advice.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS advice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sport TEXT NOT NULL,
                age TEXT NOT NULL,
                video_path TEXT,
                thumbnail_path TEXT,
                advice_text TEXT,
                practice_menu TEXT,
                is_public INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def insert_advice(sport, age, video_path, thumbnail_path, advice_text, practice_menu, is_public):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO advice (sport, age, video_path, thumbnail_path, advice_text, practice_menu, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (sport, age, str(video_path), str(thumbnail_path), advice_text, practice_menu, 1 if is_public else 0),
        )
        conn.commit()
        return cursor.lastrowid


def get_public_advice():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM advice WHERE is_public = 1 ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_advice_by_id(advice_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM advice WHERE id = ?", (advice_id,)
        ).fetchone()
    return dict(row) if row else None


def get_all_advice():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM advice ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def delete_advice(advice_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM advice WHERE id = ?", (advice_id,))
        conn.commit()
