import tkinter as tk
from tkinter import ttk

from AvailableDisplayStrategy import AvailableDisplayStrategy
from DisplayStrategy import AllDisplayStrategy
from Library import Library


def startGUI():
    root = tk.Tk()
    root.title("Online Library")
    root.geometry("760x390")
    root.resizable(False, False)

    library = Library()
    display_strategy = AllDisplayStrategy()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(
        main_frame,
        text="Online Library",
        font=("Arial", 24, "bold")
    ).pack(anchor="w")

    ttk.Label(
        main_frame,
        text="Select a book and choose an action",
        font=("Arial", 13)
    ).pack(anchor="w", pady=(5, 15))

    filter_frame = ttk.Frame(main_frame)
    filter_frame.pack(fill="x", pady=(0, 10))

    ttk.Label(filter_frame, text="Display:").pack(side="left")

    filter_var = tk.StringVar(value="All Books")
    filter_box = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=("All Books", "Available Books"),
        state="readonly",
        width=18
    )
    filter_box.pack(side="left", padx=(8, 0))

    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True)

    # Keep the table on the left and the action buttons on the right.
    table_frame = ttk.Frame(content_frame, width=585, height=245)
    table_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
    table_frame.pack_propagate(False)

    columns = ("ID", "Title", "Author", "Year", "Price", "Status")
    book_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    for column in columns:
        book_table.heading(column, text=column)

    book_table.column("ID", width=45, anchor="center")
    book_table.column("Title", width=155)
    book_table.column("Author", width=145)
    book_table.column("Year", width=55, anchor="center")
    book_table.column("Price", width=65, anchor="center")
    book_table.column("Status", width=85, anchor="center")
    book_table.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=book_table.yview
    )
    scrollbar.pack(side="right", fill="y")
    book_table.configure(yscrollcommand=scrollbar.set)

    def refresh_table():
        library.load_books()

        for item in book_table.get_children():
            book_table.delete(item)

        books_to_display = library.display_books(display_strategy)

        for book in books_to_display:
            status = "Borrowed" if book.is_borrowed else "Available"
            book_table.insert(
                "",
                tk.END,
                values=(
                    book.id,
                    book.title,
                    book.author,
                    book.year,
                    f"${book.price:.2f}",
                    status
                )
            )

    def change_display_strategy(_event=None):
        nonlocal display_strategy

        if filter_var.get() == "Available Books":
            display_strategy = AvailableDisplayStrategy()
        else:
            display_strategy = AllDisplayStrategy()

        refresh_table()

    filter_box.bind("<<ComboboxSelected>>", change_display_strategy)

    def get_selected_book():
        selected_items = book_table.selection()

        if not selected_items:
            status_label.config(text="Please select a book first.")
            return None

        values = book_table.item(selected_items[0], "values")
        return library.search_ID(int(values[0]))

    def borrow_selected():
        book = get_selected_book()
        if book is not None:
            success, message = library.borrow_book(book.id)
            status_label.config(text=message)
            refresh_table()

    def return_selected():
        book = get_selected_book()
        if book is not None:
            success, message = library.return_book(book.id)
            status_label.config(text=message)
            refresh_table()

    def buy_selected():
        book = get_selected_book()
        if book is not None:
            success, message = library.buy_book(book.id)
            status_label.config(text=message)
            refresh_table()

    button_frame = ttk.LabelFrame(
        content_frame,
        text="Actions",
        padding=10,
        width=115,
        height=245
    )
    button_frame.pack(side="right", fill="y")
    button_frame.pack_propagate(False)

    ttk.Button(
        button_frame,
        text="Borrow",
        command=borrow_selected
    ).pack(fill="x", pady=(10, 8))

    ttk.Button(
        button_frame,
        text="Return",
        command=return_selected
    ).pack(fill="x", pady=8)

    ttk.Button(
        button_frame,
        text="Buy",
        command=buy_selected
    ).pack(fill="x", pady=8)

    status_label = ttk.Label(
        main_frame,
        text="Select a book to begin.",
        foreground="green"
    )
    status_label.pack(anchor="w", pady=(12, 0))

    def close_program():
        library.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_program)
    refresh_table()
    root.mainloop()


if __name__ == "__main__":
    startGUI()
