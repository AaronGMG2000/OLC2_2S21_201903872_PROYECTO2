from pydantic import BaseModel


class RequestModel(BaseModel):
    Contenido: str
