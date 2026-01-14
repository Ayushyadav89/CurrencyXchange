from fastapi import APIRouter
from .schemas import Convert

router = APIRouter()

RATES = {
    "USD": 1,
    "INR": 83,
    "EUR": 0.91
}

@router.post("/convert")
def convert(data: Convert):
    base = data.amount / RATES[data.from_currency]
    converted = base * RATES[data.to_currency]
    return {"converted_amount": converted}
