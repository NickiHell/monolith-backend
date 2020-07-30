from pydantic.main import BaseModel


class Status(BaseModel):
    message: str
