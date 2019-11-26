class AppException(Exception):

    def __init__(self, message, http_code):
        super(Exception, self).__init__(message)
        self.message = message
        self.http_code = http_code
