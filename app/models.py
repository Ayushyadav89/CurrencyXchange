from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    profile_photo = Column(String(200), nullable=True)

    # Relationship with Wallet
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete")
    # Relationship with Transactions
    sent_transactions = relationship("Transaction", back_populates="sender", foreign_keys="Transaction.sender_id")
    received_transactions = relationship("Transaction", back_populates="receiver", foreign_keys="Transaction.receiver_id")


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String(10), nullable=False)
    balance = Column(Float, default=0)

    # Relationship with User
    user = relationship("User", back_populates="wallets")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_currency = Column(String(10), nullable=False)
    to_currency = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    converted_amount = Column(Float, nullable=False)

    # Relationships
    sender = relationship("User", back_populates="sent_transactions", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_transactions", foreign_keys=[receiver_id])
