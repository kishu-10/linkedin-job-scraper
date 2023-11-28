from fastapi.responses import JSONResponse


class Response:
    def __init__(self, status_code: int, message: str, data: any):
        self.status_code = status_code
        self.message = message
        self.data = data

    def __repr__(self):
        return JSONResponse(
            content={
                "message": self.message,
                "status_code": self.status_code,
                "data": self.data,
            }
        )
