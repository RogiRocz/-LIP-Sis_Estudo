from pydantic import BaseModel
from src.schemas.user import User

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
