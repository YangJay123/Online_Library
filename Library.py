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
                self.borrow_history.append(book)
                print(f"You have borrowed '{book.title}'.")
                book.borrow_date = date.today()
                book.due_date = book.borrow_date + timedelta(days=14)
                print(f"Borrowed on {book.borrow_date} and due on {book.due_date}")
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


    def buy_book(self, id):
        book = self.search_ID(id)
        if book is not None:
            if book.is_borrowed:
                print("Cannot purchase a borrowed book.")
            else:
                print(f"You have purchased '{book.title}' for ${book.price:.2f}.")
                self.books.remove(book)
                self.purchase_history.append(book)
        else:
            print("Book not found.")

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
        category_counts = {
            "Horror": 2,
            "Textbook": 1,
            "General": 3
        }
        for book in history:
            category = book.category.lower()
            if category in category_counts:
                category_counts[category] += 1
        else:
            category_counts[category] = 1
        max_count = max(category_counts.values())

        for book in self.books:
            if book.category.lower() in category_counts and category_counts[book.category.lower()] == max_count:
                recommendations.append(book)
        return recommendations