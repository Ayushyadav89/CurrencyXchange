from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class WalletCreate(BaseModel):
    currency: str
    balance: float

class Convert(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class Transfer(BaseModel):
    receiver_id: int
    from_currency: str
    to_currency: str
    amount: float
