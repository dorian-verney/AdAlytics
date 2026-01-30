from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class UserOut(User):
    id: int

class TextEntry(BaseModel):
    main_text: str
    additional_context: str