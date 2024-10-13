class ApiErrorResponse:
    def __init__(self, error):
        self.error = error.__class__.__name__
        self.message = str(error)

    def to_dict(self):
        return {
            'error': self.error,
            'message': self.message
        }
