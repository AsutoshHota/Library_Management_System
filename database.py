import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).with_name("library.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, author TEXT NOT NULL, category TEXT NOT NULL,
            total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
            available_copies INTEGER NOT NULL CHECK(available_copies BETWEEN 0 AND total_copies)
        );
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone TEXT
        );
        CREATE TABLE IF NOT EXISTS issue_records (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL REFERENCES books(book_id),
            member_id INTEGER NOT NULL REFERENCES members(member_id),
            issue_date TEXT NOT NULL, return_date TEXT,
            status TEXT NOT NULL DEFAULT 'ISSUED' CHECK(status IN ('ISSUED','RETURNED'))
        );
        """)
