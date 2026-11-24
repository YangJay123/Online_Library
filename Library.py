from datetime import date, timedelta
class Library:
    def __init__(self):
        self.books = []
        self.borrow_history = []
        self.purchase_history = []
        self.last_return_fine = 0.0

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        i = 1
        for book in self.books:
            print (f"{i}")
            book.display_info()
            i += 1
            print()  
      
    def search_ID(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None

    def borrow_book(self, id):
        book = self.search_ID(id)
        if book is not None:
            if not book.is_borrowed:
                book.is_borrowed = True
                self.borrow_history.append(book)
                print(f"You have borrowed '{book.title}'.")
                book.borrow_date = date.today()
                book.due_date = book.borrow_date + timedelta(days=14)
                print(f"Borrowed on {book.borrow_date} and due on {book.due_date}")
                return True
            else:
                print(f"'{book.title}' is already borrowed.")
                return False
        else:
            print("Book not found.")
            return False

    def return_book(self, id):
        self.last_return_fine = 0.0
        book = self.search_ID(id)
        if book is not None:
            if book.is_borrowed:
                if date.today() > book.due_date:
                    difference = date.today() - book.due_date
                    print(f"Overdue by {difference.days} days")
                    fine = difference.days * 0.5
                    self.last_return_fine = fine
                    print(f"You are fined ${fine:.2f}")
                book.is_borrowed = False
                book.borrow_date = None
                book.due_date = None
                print(f"You have returned '{book.title}'.")
                return True
            else:
                print("Book is not currently borrowed")
                return False
        else:
            print("Book does not exist")
            return False


    def buy_book(self, id):
        book = self.search_ID(id)
        if book is not None:
            if book.is_borrowed:
                print("Cannot purchase a borrowed book.")
                return False
            else:
                print(f"You have purchased '{book.title}' for ${book.price:.2f}.")
                self.books.remove(book)
                self.purchase_history.append(book)
                return True
        else:
            print("Book not found.")
            return False

    def search_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def seasonal_recommendations(self):
        month = date.today().month
        recommendations = []
        if month == 12:
             category = "Christmas"
        elif month == 10:
             category = "Halloween"
        elif month == 8:
            category = "Textbook"
        else:
            category = "General"
        for book in self.books:
            if book.category.lower() == category.lower():
                recommendations.append(book)
        return recommendations

    def personalized_recommendations(self):
        history = self.borrow_history + self.purchase_history
        if not history:
            return []
        recommendations = []
        category_counts = {}
        for book in history:
            category = book.category.lower()
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
        max_count = max(category_counts.values())

        for book in self.books:
            category = book.category.lower()
            if category in category_counts and category_counts[category] == max_count and book not in history and not book.is_borrowed:
                recommendations.append(book)
        return recommendations