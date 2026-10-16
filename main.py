from Book import Book
from Library import Library
library = Library()
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 10.99, 1)
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960, 7.99, 2)
book3 = Book("1984", "George Orwell", 1949, 8.99, 3)
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.display_books()

#library.search_ID(-1)
library.borrow_book(1)
library.return_book(2)