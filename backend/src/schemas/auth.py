from pydantic import BaseModel
from .user import User

class Token(BaseModel):
    token: str
    token_type: str
    user: User
