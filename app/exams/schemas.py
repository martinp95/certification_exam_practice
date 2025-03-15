from pydantic import BaseModel
from typing import Optional
import uuid

class CertificationSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str

    class Config:
        from_attrinutes = True # Allows conversion from SQLAlchemy models