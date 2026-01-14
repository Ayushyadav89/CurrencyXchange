from fastapi import FastAPI
from .database import Base, engine
from . import auth, wallet, currency, transfer

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CurrencyXchange")

app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(currency.router)
app.include_router(transfer.router)
