from pydantic import BaseModel


class ErrorData(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorData
