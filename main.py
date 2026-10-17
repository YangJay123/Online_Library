import tkinter as tk
from tkinter import ttk

from Book import Book
from Library import Library


def initializeLibrary():
    library = Library()
    library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 10.99, 1))
    library.add_book(Book("To Kill a Mockingbird", "Harper Lee", 1960, 7.99, 2))
    library.add_book(Book("1984", "George Orwell", 1949, 8.99, 3))
    return library


def startGUI():
    root = tk.Tk()
    root.title("Online Library")
    root.geometry("500x350")

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Online Library",
        font=("Arial", 22, "bold"),
    ).pack(anchor="w")

    ttk.Label(
        frame,
        text="Available books",
        font=("Arial", 12),
    ).pack(anchor="w", pady=(4, 10))

    book_list = tk.Listbox(frame, font=("Arial", 13), height=10)
    book_list.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=book_list.yview)
    scrollbar.pack(side="right", fill="y")
    book_list.config(yscrollcommand=scrollbar.set)

    library = initializeLibrary()
    for book in library.books:
        book_list.insert(tk.END, book.title)

    root.mainloop()


if __name__ == "__main__":
    startGUI()
