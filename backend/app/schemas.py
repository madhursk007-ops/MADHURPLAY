from pydantic import BaseModel, EmailStr, ConfigDict

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WatchlistIn(BaseModel):
    movie_id: int
    title: str
    poster_path: str | None = None

class WatchlistOut(WatchlistIn):
    id: int
    model_config = ConfigDict(from_attributes=True)
