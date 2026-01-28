from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class UserOut(User):
    id: int