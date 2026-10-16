class Book:
    def __init__(self, title, author, year, price, id,):
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.id = id
        self.is_borrowed = False
        self.borrowed_date = None
        self.due_date = None

    def display_info(self):
        if self == None:
            print("Book not found.")
            return
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Year: {self.year}")
        print(f"Price: ${self.price:.2f}")
        print(f"ID: {self.id}")
        print(f"Borrowed: {'Yes' if self.is_borrowed else 'No'}")

    


  