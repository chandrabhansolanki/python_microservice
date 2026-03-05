from pydantic import BaseModel
from typing import Optional

class ResumeResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]