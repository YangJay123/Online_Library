class Book:
    def __init__(self, title, author, year, price, id, category="General"):
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.id = id
        self.is_borrowed = False
        self.borrow_date = None
        self.due_date = None
        self.category = category

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Year: {self.year}")
        print(f"Price: ${self.price:.2f}")
        print(f"ID: {self.id}")
        print(f"Borrowed: {'Yes' if self.is_borrowed else 'No'}")

    


  