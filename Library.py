import sqlite3
from datetime import date, timedelta

from Book import Book


class Library:
    def __init__(self, database_name="library.db"):
        self.database_name = database_name
        self.books = []
        self.connection = sqlite3.connect(self.database_name)
        self._create_tables()
        self._seed_database_if_needed()
        self.load_books()

    def _create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                is_borrowed INTEGER NOT NULL DEFAULT 0,
                borrowed_date TEXT,
                due_date TEXT
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def _seed_database_if_needed(self):
        seeded = self.connection.execute(
            "SELECT value FROM settings WHERE name = 'sample_books_added'"
        ).fetchone()

        if seeded is None:
            sample_books = [
                ("The Great Gatsby", "F. Scott Fitzgerald", 1925, 10.99, 1),
                ("To Kill a Mockingbird", "Harper Lee", 1960, 7.99, 2),
                ("1984", "George Orwell", 1949, 8.99, 3),
            ]
            self.connection.executemany(
                """
                INSERT OR IGNORE INTO books
                    (title, author, year, price, id)
                VALUES (?, ?, ?, ?, ?)
                """,
                sample_books,
            )
            self.connection.execute(
                "INSERT INTO settings (name, value) VALUES (?, ?)",
                ("sample_books_added", "1"),
            )
            self.connection.commit()

    def load_books(self):
        rows = self.connection.execute(
            """
            SELECT id, title, author, year, price, is_borrowed,
                   borrowed_date, due_date
            FROM books
            ORDER BY id
            """
        ).fetchall()

        self.books = []
        for row in rows:
            book = Book(row[1], row[2], row[3], row[4], row[0])
            book.is_borrowed = bool(row[5])
            book.borrowed_date = (
                date.fromisoformat(row[6]) if row[6] else None
            )
            book.due_date = date.fromisoformat(row[7]) if row[7] else None
            self.books.append(book)

    def close(self):
        self.connection.close()

    def add_book(self, book):
        self.books.append(book)
        self.connection.execute(
            """
            INSERT INTO books (id, title, author, year, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            (book.id, book.title, book.author, book.year, book.price),
        )
        self.connection.commit()

    def display_books(self, display_strategy):
        """Use a strategy to choose which books should be displayed."""
        return display_strategy.display_books(self.books)
      
    def search_ID(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None

    def borrow_book(self, id):
        book = self.search_ID(id)
        if book is None:
            return False, "Book not found."
        if book.is_borrowed:
            return False, f"'{book.title}' is already borrowed."
        book.is_borrowed = True
        book.borrowed_date = date.today()
        book.due_date = book.borrowed_date + timedelta(days=14)
        self.connection.execute(
            """
            UPDATE books
            SET is_borrowed = 1, borrowed_date = ?, due_date = ?
            WHERE id = ?
            """,
            (book.borrowed_date.isoformat(), book.due_date.isoformat(), book.id),
        )
        self.connection.commit()
        return True, f"You borrowed '{book.title}'. Due date: {book.due_date}."
            
    def return_book(self, id):
        book = self.search_ID(id)
        if book is None:
            return False, "Book does not exist."
        if not book.is_borrowed:
            return False, "Book is not currently borrowed."
        fine = 0.0
        if date.today() > book.due_date:
            fine = (date.today() - book.due_date).days * 0.50
        book.is_borrowed = False
        book.borrowed_date = None
        book.due_date = None
        self.connection.execute(
            """
            UPDATE books
            SET is_borrowed = 0, borrowed_date = NULL, due_date = NULL
            WHERE id = ?
            """,
            (book.id,),
        )
        self.connection.commit()
        if fine:
            return True, f"You returned '{book.title}'. Overdue fine: ${fine:.2f}."
        return True, f"You returned '{book.title}' with no fine."

    def buy_book(self, id):
        book = self.search_ID(id)
        if book is None:
            return False, "Book does not exist."
        self.books.remove(book)
        self.connection.execute("DELETE FROM books WHERE id = ?", (book.id,))
        self.connection.commit()
        return True, f"You bought '{book.title}' for ${book.price:.2f}."
