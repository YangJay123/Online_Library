from datetime import date, timedelta
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        i = 1
        for book in self.books:
            print (f"{i}")
            print(f"{book.display_info()}")
            i += 1
            print()  
      
    def search_ID(self, id):
        for book in self.books:
            if book.id == id:
                book.display_info()
                return book
        return None

    def borrow_book(self, id):
        book = self.search_ID(id)
        if book is not None:
            if not book.is_borrowed:
                book.is_borrowed = True
                print(f"You have borrowed '{book.title}'.")
                self.borrowed_date = date.today()
                self.due_date = self.borrowed_date + timedelta(days=14)
                print(f"Borrowed on {self.borrowed_date} and due on {self.due_date}")
            else:
                print(f"'{book.title}' is already borrowed.")
        else:
            print("Book not found.")
            
    def return_book(self, id):
        book = self.search_ID(id)
        if book is not None:
            if book.is_borrowed:
                if date.today() > book.due_date:
                    difference = date.today() - book.due_date
                    print(f"Overdue by {difference.days} days")
                    book.is_borrowed = False
                    book.borrow_date = None
                    book.due_date = None
                    fine = difference.days * 0.5
                    print(f"You are fined ${fine:.2f}")
                    print(f"You have returned '{book.title}'.")
                else:
                     book.is_borrowed = False
                     book.borrow_date = None
                     book.due_date = None
                     print(f"You have returned '{book.title}'.")
            else:
                print("Book is not currently borrowed")
        else:
            print("Book does not exist")