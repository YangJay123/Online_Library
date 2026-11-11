from DisplayStrategy import DisplayStrategy


class AvailableDisplayStrategy(DisplayStrategy):

    def display_books(self, books):
        return [
            book for book in books
            if not book.is_borrowed
        ]
