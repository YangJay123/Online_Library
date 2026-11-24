import sqlite3
from datetime import date, timedelta

from Book import Book


class Library:
    def __init__(self, database_name="library.db"):
        self.database_name = database_name
        self.books = []
        self.borrow_history = []
        self.purchase_history = []
        self.last_return_fine = 0.0

        self.connection = sqlite3.connect(self.database_name)
        self._create_tables()
        self._seed_database_if_needed()
        self._seed_extra_books_if_needed()
        self.load_books()
        self._load_history()

    def _create_tables(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                is_borrowed INTEGER NOT NULL DEFAULT 0,
                borrowed_date TEXT,
                due_date TEXT,
                category TEXT NOT NULL DEFAULT 'General'
            )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS history (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                book_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL DEFAULT 'General'
            )
        """)

        # Update databases created before categories were introduced.
        columns = {
            row[1] for row in self.connection.execute("PRAGMA table_info(books)")
        }
        if "category" not in columns:
            self.connection.execute(
                "ALTER TABLE books ADD COLUMN category TEXT NOT NULL DEFAULT 'General'"
            )
        self.connection.commit()

    def _seed_database_if_needed(self):
        seeded = self.connection.execute(
            "SELECT value FROM settings WHERE name = 'sample_books_added'"
        ).fetchone()
        if seeded is not None:
            return

        samples = [
            (1, "The Great Gatsby", "F. Scott Fitzgerald", 1925, 10.99, "General"),
            (2, "To Kill a Mockingbird", "Harper Lee", 1960, 7.99, "General"),
            (3, "1984", "George Orwell", 1949, 8.99, "General"),
        ]
        with self.connection:
            self.connection.executemany("""
                INSERT OR IGNORE INTO books (id, title, author, year, price, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, samples)
            self.connection.execute(
                "INSERT INTO settings (name, value) VALUES (?, ?)",
                ("sample_books_added", "1"),
            )
    def _seed_extra_books_if_needed(self):
        seeded = self.connection.execute(
            "SELECT value FROM settings WHERE name = 'extra_books_added'"
        ).fetchone()
        if seeded is not None:
            return
        extra_books = [
            (4, "A Christmas Carol", "Charles Dickens", 1843, 5.99, "Christmas"),
            (5, "The Nightmare Before Christmas", "Tim Burton", 1993, 6.99, "Christmas"),
            (6, "The Shining", "Stephen King", 1977, 12.99, "Horror"),
            (7, "Dracula", "Bram Stoker", 1897, 9.99, "Horror"),
            (8, "Frankenstein", "Mary Shelley", 1818, 8.99, "Horror"),
            (9, "Calculus: Early Transcendentals", "James Stewart", 2007, 150.00, "Textbook"),
            (10, "Introduction to Algorithms", "Thomas H. Cormen", 2009, 80.00, "Textbook"),
        ]
        with self.connection:
            self.connection.executemany("""
                INSERT OR IGNORE INTO books (id, title, author, year, price, category)
                VALUES (?, ?, ?, ?, ?, ?)
                """, extra_books)
            self.connection.execute(
                "INSERT INTO settings (name, value) VALUES (?, ?)",
                ("extra_books_added", "1"),
            )

    def load_books(self):
        rows = self.connection.execute("""
            SELECT id, title, author, year, price, is_borrowed,
                   borrowed_date, due_date, category
            FROM books ORDER BY id
        """).fetchall()

        self.books = []
        for row in rows:
            book = Book(row[1], row[2], row[3], row[4], row[0], row[8])
            book.is_borrowed = bool(row[5])
            book.borrow_date = date.fromisoformat(row[6]) if row[6] else None
            book.due_date = date.fromisoformat(row[7]) if row[7] else None
            self.books.append(book)

    def _load_history(self):
        self.borrow_history = []
        self.purchase_history = []
        rows = self.connection.execute("""
            SELECT action, book_id, title, author, year, price, category
            FROM history ORDER BY event_id
        """).fetchall()
        for action, book_id, title, author, year, price, category in rows:
            book = Book(title, author, year, price, book_id, category)
            if action == "borrow":
                self.borrow_history.append(book)
            elif action == "purchase":
                self.purchase_history.append(book)

    def _record_history(self, action, book):
        self.connection.execute("""
            INSERT INTO history (action, book_id, title, author, year, price, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            action, book.id, book.title, book.author, book.year,
            book.price, book.category,
        ))

    def close(self):
        self.connection.close()

    def add_book(self, book):
        with self.connection:
            self.connection.execute("""
                INSERT INTO books (id, title, author, year, price, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                book.id, book.title, book.author, book.year,
                book.price, book.category,
            ))
        self.books.append(book)

    def display_books(self, display_strategy=None):
        if display_strategy is not None:
            return display_strategy.display_books(self.books)
        for i, book in enumerate(self.books, start=1):
            print(i)
            book.display_info()
            print()

    def search_ID(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None

    def search_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, id):
        book = self.search_ID(id)
        if book is None:
            return False, "Book not found."
        if book.is_borrowed:
            return False, f"'{book.title}' is already borrowed."

        borrowed = date.today()
        due = borrowed + timedelta(days=14)
        with self.connection:
            self.connection.execute("""
                UPDATE books SET is_borrowed = 1, borrowed_date = ?, due_date = ?
                WHERE id = ?
            """, (borrowed.isoformat(), due.isoformat(), book.id))
            self._record_history("borrow", book)

        book.is_borrowed = True
        book.borrow_date = borrowed
        book.due_date = due
        self.borrow_history.append(book)
        return True, f"You borrowed '{book.title}'. Due date: {book.due_date}."

    def return_book(self, id):
        self.last_return_fine = 0.0
        book = self.search_ID(id)
        if book is None:
            return False, "Book does not exist."
        if not book.is_borrowed:
            return False, "Book is not currently borrowed."

        fine = 0.0
        if book.due_date is not None and date.today() > book.due_date:
            fine = (date.today() - book.due_date).days * 0.50

        with self.connection:
            self.connection.execute("""
                UPDATE books
                SET is_borrowed = 0, borrowed_date = NULL, due_date = NULL
                WHERE id = ?
            """, (book.id,))

        book.is_borrowed = False
        book.borrow_date = None
        book.due_date = None
        self.last_return_fine = fine
        if fine > 0:
            return True, f"You returned '{book.title}'. Overdue fine: ${fine:.2f}."
        return True, f"You returned '{book.title}' with no fine."

    def buy_book(self, id):
        book = self.search_ID(id)
        if book is None:
            return False, "Book not found."
        if book.is_borrowed:
            return False, "Cannot purchase a borrowed book."

        with self.connection:
            self.connection.execute("DELETE FROM books WHERE id = ?", (book.id,))
            self._record_history("purchase", book)
        self.books.remove(book)
        self.purchase_history.append(book)
        return True, f"You bought '{book.title}' for ${book.price:.2f}."

    def seasonal_recommendations(self):
        month = date.today().month
        if month == 12:
            category = "Christmas"
        elif month == 10:
            category = "Horror"
        elif month == 8:
            category = "Textbook"
        else:
            category = "General"
        return [
            book for book in self.books
            if book.category.lower() == category.lower() and not book.is_borrowed
        ]

    def personalized_recommendations(self):
        history = self.borrow_history + self.purchase_history
        if not history:
            return []

        category_counts = {}
        for book in history:
            category = book.category.lower()
            category_counts[category] = category_counts.get(category, 0) + 1

        max_count = max(category_counts.values())
        previously_used_ids = {book.id for book in history}
        return [
            book for book in self.books
            if book.category.lower() in category_counts
            and category_counts[book.category.lower()] == max_count
            and book.id not in previously_used_ids
            and not book.is_borrowed
        ]

   