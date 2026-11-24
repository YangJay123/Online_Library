
from Book import Book
from Library import Library
from datetime import date, timedelta

# Initialize library
library = Library()

# Create books
book1 = Book("Dracula", "Bram Stoker", 1897, 9.99, 1, "Horror")
book2 = Book("Frankenstein", "Mary Shelley", 1818, 8.99, 2, "Horror")
book3 = Book("Python Basics", "John Smith", 2020, 19.99, 3, "Textbook")
book4 = Book("The Shining", "Stephen King", 1977, 12.99, 4, "Horror")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)


# TEST 1: Display Books
print("\n===== TEST 1: DISPLAY BOOKS =====")
library.display_books()
print("TEST 1 PASSED!")


# TEST 2: Search
print("\n===== TEST 2: SEARCH =====")
assert library.search_ID(1) == book1
assert library.search_title("DRACULA") == book1
assert library.search_ID(99) is None
print("TEST 2 PASSED!")


# TEST 3: Borrow
print("\n===== TEST 3: BORROW =====")
assert library.borrow_book(1) is True
assert library.borrow_book(1) is False

assert book1.is_borrowed is True
assert book1.borrow_date == date.today()
assert book1.due_date == date.today() + timedelta(days=14)

print("TEST 3 PASSED!")


# TEST 4: Return
print("\n===== TEST 4: RETURN =====")
assert library.return_book(1) is True
assert library.return_book(1) is False

assert book1.is_borrowed is False
assert book1.borrow_date is None
assert book1.due_date is None

print("TEST 4 PASSED!")


# TEST 5: Overdue Fine
print("\n===== TEST 5: OVERDUE FINE =====")
library.borrow_book(1)
book1.due_date = date.today() - timedelta(days=4)

assert library.return_book(1) is True
assert book1.is_borrowed is False
assert book1.due_date is None
assert library.last_return_fine == 2.0

print("TEST 5 PASSED!")


# TEST 6: Purchase
print("\n===== TEST 6: PURCHASE =====")
assert library.buy_book(2) is True

assert library.search_ID(2) is None
assert book2 in library.purchase_history

print("TEST 6 PASSED!")


# TEST 7: Personalized Recommendations
print("\n===== TEST 7: RECOMMENDATIONS =====")
recommended = library.personalized_recommendations()

for book in recommended:
    print("Recommended:", book.title)

assert book4 in recommended
assert book1 not in recommended

print("TEST 7 PASSED!")


# TEST 8: History
print("\n===== TEST 8: HISTORY =====")
print("Borrow history:", len(library.borrow_history))
print("Purchase history:", len(library.purchase_history))

assert len(library.borrow_history) == 2
assert len(library.purchase_history) == 1

print("TEST 8 PASSED!")


# TEST 9: Boolean Return Values
print("\n===== TEST 9: BOOLEAN RETURN VALUES =====")

test_book = Book("Test Book", "Test Author", 2026, 5.99, 99)
library.add_book(test_book)

# Borrowing
assert library.borrow_book(99) is True
assert library.borrow_book(99) is False

# Returning
assert library.return_book(99) is True
assert library.return_book(99) is False

# Purchasing
assert library.buy_book(99) is True
assert library.buy_book(99) is False

# Invalid book
assert library.borrow_book(999) is False
assert library.return_book(999) is False
assert library.buy_book(999) is False

print("TEST 9 PASSED!")


# TEST 10: Fine Tracking
print("\n===== TEST 10: FINE TRACKING =====")

book5 = Book("Fine Test", "Test Author", 2026, 5.99, 100)
library.add_book(book5)

# Test overdue return
library.borrow_book(100)
book5.due_date = date.today() - timedelta(days=4)
library.return_book(100)

assert library.last_return_fine == 2.0
print("Overdue fine test passed!")

# Test on-time return
library.borrow_book(100)
library.return_book(100)

assert library.last_return_fine == 0.0
print("On-time return fine test passed!")

# Test invalid return
library.return_book(999)

assert library.last_return_fine == 0.0
print("Invalid return fine test passed!")

print("TEST 10 PASSED!")


print("\n===== ALL 10 TESTS PASSED! =====")
