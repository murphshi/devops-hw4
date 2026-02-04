import os
import sqlite3
from flask import Flask, jsonify, request, g

DB_PATH = os.getenv("DB_PATH", "app.db")

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    """
    Create a connection per request and reuse it via Flask g.
    """
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """
    Create tables if they do not exist.
    """
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON;")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    db.commit()
    db.close()


@app.get("/")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/api/notes")
def create_note():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    body = (data.get("body") or "").strip()

    if not title or not body:
        return jsonify({"error": "title and body are required"}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO note (title, body) VALUES (?, ?)",
        (title, body),
    )
    db.commit()

    return jsonify({"id": cur.lastrowid, "title": title, "body": body}), 201


@app.get("/api/notes")
def list_notes():
    db = get_db()
    rows = db.execute("SELECT id, title, body, created_at FROM note ORDER BY id;").fetchall()
    notes = [dict(r) for r in rows]
    return jsonify(notes), 200


@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id: int):
    db = get_db()
    cur = db.execute("DELETE FROM note WHERE id = ?", (note_id,))
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
