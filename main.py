from database import initialize_database
from library import Library

def integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Enter a valid whole number.")

def print_books(rows):
    if not rows:
        print("No books found.")
    for b in rows:
        print(f"ID {b['book_id']} | {b['title']} | {b['author']} | "
              f"{b['category']} | Available {b['available_copies']}/{b['total_copies']}")

def print_members(rows):
    if not rows:
        print("No members found.")
    for m in rows:
        print(f"ID {m['member_id']} | {m['name']} | {m['email']} | {m['phone'] or '-'}")

def print_records(rows):
    if not rows:
        print("No issue records found.")
    for r in rows:
        print(f"Issue {r['issue_id']} | {r['title']} | {r['member_name']} | "
              f"Issued: {r['issue_date']} | Returned: {r['return_date'] or '-'} | {r['status']}")

def main():
    initialize_database()
    lib = Library()
    while True:
        print("""
====== LIBRARY MANAGEMENT SYSTEM ======
1. Add book
2. Search/view books
3. Register member
4. View members
5. Issue book
6. Return book
7. View all issue records
8. View active issues
0. Exit
""")
        choice = input("Select option: ").strip()
        try:
            if choice == "1":
                lib.add_book(input("Title: "), input("Author: "), input("Category: "),
                             integer("Number of copies: "))
                print("Book added.")
            elif choice == "2":
                print_books(lib.list_books(input("Search (blank = all): ")))
            elif choice == "3":
                lib.add_member(input("Member name: "), input("Email: "), input("Phone: "))
                print("Member registered.")
            elif choice == "4":
                print_members(lib.list_members())
            elif choice == "5":
                print_books(lib.list_books())
                book_id = integer("Book ID: ")
                print_members(lib.list_members())
                member_id = integer("Member ID: ")
                lib.issue_book(book_id, member_id)
                print("Book issued successfully.")
            elif choice == "6":
                print_records(lib.list_issue_records(active_only=True))
                lib.return_book(integer("Issue ID to return: "))
                print("Book returned successfully.")
            elif choice == "7":
                print_records(lib.list_issue_records())
            elif choice == "8":
                print_records(lib.list_issue_records(active_only=True))
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Choose a valid menu option.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Operation failed: {exc}")

if __name__ == "__main__":
    main()
