# Library Management System

A working, menu-driven Library Management System built with Python, OOP and SQLite (SQL).

## Features
- Add and search books by title, author or category.
- Register and view library members.
- Issue books and automatically reduce available copies.
- Return books and automatically restore available copies.
- View all issue records and currently active issues.
- Input validation and error handling.
- Persistent storage in a local SQLite database.

## Requirements
- Python 3.8+
- No third-party packages required (`sqlite3` is included with Python).

## Run
Open a terminal in this folder and execute:

```bash
python main.py
```

The `library.db` database is created automatically the first time the program runs.

## Quick test
1. Choose `1` to add a book; enter a title, author, category and copies.
2. Choose `3` to register a member with a unique email.
3. Choose `5` to issue a book using the displayed book and member IDs.
4. Choose `8` to confirm the active issue.
5. Choose `6` and enter the issue ID to return it.
6. Choose `2` to verify the available copy count is restored.

## Database design
- `books`: book details and total/available copy counts.
- `members`: member name, unique email and phone.
- `issue_records`: book/member references, issue date, return date and status.

## Source structure
```text
library_management_system/
├── main.py
├── library.py
├── database.py
└── README.md
```

## CV project description
**Library Management System | Python, OOP, SQLite**

- Developed a menu-driven Library Management System using Python and Object-Oriented Programming.
- Implemented book and member management features, including adding, searching and viewing records.
- Integrated SQLite to store book details, member information and issue/return transactions.
- Implemented book availability tracking, input validation and error handling to prevent invalid issue and return operations.

Only list features on your CV after running the project and being able to explain the implementation.
