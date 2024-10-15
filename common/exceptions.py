from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, message = 'Not found'):
        super().__init__(status_code=404, detail=message)
    
class BadRequestException(HTTPException):
    def __init__(self, message = 'Bad request'):
        super().__init__(status_code=400, detail=message)