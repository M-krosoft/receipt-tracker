class ApiErrorResponse:
    def __init__(self, error):
        self.error = error.__class__.__name__
        self.message = str(error)

    def to_dictionary(self):
        return {
            'error': self.error,
            'message': self.message
        }
