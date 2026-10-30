from datetime import date
from database import get_connection

class Library:
    """Library operations implemented with a small OOP service class."""

    def add_book(self, title, author, category, copies):
        if not all(x.strip() for x in (title, author, category)):
            raise ValueError("Title, author and category are required.")
        if copies < 1:
            raise ValueError("Copies must be at least 1.")
        with get_connection() as conn:
            conn.execute("""INSERT INTO books
                (title, author, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?)""",
                (title.strip(), author.strip(), category.strip(), copies, copies))

    def list_books(self, search=""):
        with get_connection() as conn:
            if search.strip():
                p = f"%{search.strip()}%"
                return conn.execute("""SELECT * FROM books
                    WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
                    ORDER BY title""", (p, p, p)).fetchall()
            return conn.execute("SELECT * FROM books ORDER BY title").fetchall()

    def add_member(self, name, email, phone=""):
        if not name.strip() or not email.strip():
            raise ValueError("Name and email are required.")
        with get_connection() as conn:
            conn.execute("INSERT INTO members(name,email,phone) VALUES(?,?,?)",
                         (name.strip(), email.strip().lower(), phone.strip()))

    def list_members(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM members ORDER BY name").fetchall()

    def issue_book(self, book_id, member_id):
        with get_connection() as conn:
            book = conn.execute("SELECT available_copies FROM books WHERE book_id=?",
                                (book_id,)).fetchone()
            member = conn.execute("SELECT member_id FROM members WHERE member_id=?",
                                  (member_id,)).fetchone()
            if book is None:
                raise ValueError("Book ID not found.")
            if member is None:
                raise ValueError("Member ID not found.")
            if book["available_copies"] < 1:
                raise ValueError("No copies currently available.")
            conn.execute("""INSERT INTO issue_records(book_id,member_id,issue_date,status)
                            VALUES(?,?,?,'ISSUED')""",
                         (book_id, member_id, date.today().isoformat()))
            conn.execute("UPDATE books SET available_copies=available_copies-1 WHERE book_id=?",
                         (book_id,))

    def return_book(self, issue_id):
        with get_connection() as conn:
            record = conn.execute("SELECT book_id,status FROM issue_records WHERE issue_id=?",
                                  (issue_id,)).fetchone()
            if record is None:
                raise ValueError("Issue record not found.")
            if record["status"] == "RETURNED":
                raise ValueError("This book has already been returned.")
            conn.execute("""UPDATE issue_records SET status='RETURNED', return_date=?
                            WHERE issue_id=?""", (date.today().isoformat(), issue_id))
            conn.execute("UPDATE books SET available_copies=available_copies+1 WHERE book_id=?",
                         (record["book_id"],))

    def list_issue_records(self, active_only=False):
        sql = """SELECT ir.issue_id,b.title,m.name AS member_name,ir.issue_date,
                        ir.return_date,ir.status
                 FROM issue_records ir
                 JOIN books b ON b.book_id=ir.book_id
                 JOIN members m ON m.member_id=ir.member_id"""
        if active_only:
            sql += " WHERE ir.status='ISSUED'"
        sql += " ORDER BY ir.issue_id DESC"
        with get_connection() as conn:
            return conn.execute(sql).fetchall()
