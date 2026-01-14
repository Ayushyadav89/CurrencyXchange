from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Wallet
from .schemas import WalletCreate


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/wallet/{user_id}")
def create_wallet(user_id: int, wallet: WalletCreate, db: Session = Depends(get_db)):
    w = Wallet(user_id=user_id, currency=wallet.currency, balance=wallet.balance)
    db.add(w)
    db.commit()
    return {"message": "Wallet created"}

@router.get("/wallet/{user_id}")
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()
