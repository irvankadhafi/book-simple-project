class BookNotFoundError(Exception):
    pass

class InvalidBookDataError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"Invalid book data: {errors}")
