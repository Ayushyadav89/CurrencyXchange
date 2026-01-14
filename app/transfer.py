from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Wallet, Transaction
from .schemas import Transfer


router = APIRouter()

RATES = {"USD": 1, "INR": 83, "EUR": 0.91}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transfer/{sender_id}")
def transfer(sender_id: int, data: Transfer, db: Session = Depends(get_db)):
    sender_wallet = db.query(Wallet).filter(
        Wallet.user_id == sender_id,
        Wallet.currency == data.from_currency
    ).first()

    if not sender_wallet or sender_wallet.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    receiver_wallet = db.query(Wallet).filter(
        Wallet.user_id == data.receiver_id,
        Wallet.currency == data.to_currency
    ).first()

    converted = (data.amount / RATES[data.from_currency]) * RATES[data.to_currency]

    sender_wallet.balance -= data.amount
    receiver_wallet.balance += converted

    txn = Transaction(
        sender_id=sender_id,
        receiver_id=data.receiver_id,
        from_currency=data.from_currency,
        to_currency=data.to_currency,
        amount=data.amount,
        converted_amount=converted
    )

    db.add(txn)
    db.commit()
    return {"message": "Transfer successful"}
