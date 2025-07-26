from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()


class TransactionTypeEnum(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = db.relationship("Transactions", back_populates="users", lazy=True)
    holdings = db.relationship("Holdings", back_populates="users", lazy=True)


class Constants(db.Model):
    __tablename__ = "Constants"

    name = db.Column(db.String(50), primary_key=True, nullable=False)
    description = db.Column(db.Text)


class Assets(db.Model):
    __tablename__ = "Assets"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(50))
    investment_type = db.Column(db.String(36), db.ForeignKey("Constants.name"))
    currency = db.Column(db.String(10))
    platform = db.Column(db.String(50))
    custom_data = db.Column(db.JSON)

    transactions = db.relationship("Transactions", back_populates="assets", lazy=True)
    holdings = db.relationship("Holdings", back_populates="assets", lazy=True)
    price_history = db.relationship("Price_History", back_populates="assets", lazy=True)


class Transactions(db.Model):
    __tablename__ = "Transactions"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("Users.id"))
    asset_id = db.Column(db.String(36), db.ForeignKey("Assets.id"), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionTypeEnum), nullable=False)
    quantity = db.Column(db.Numeric(18, 6), nullable=False)
    price_per_unit = db.Column(db.Numeric(18, 2), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    users = db.relationship("Users", back_populates="transactions")
    assets = db.relationship("Assets", back_populates="transactions")


class Holdings(db.Model):
    __tablename__ = "Holdings"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("Users.id"))
    asset_id = db.Column(db.String(36), db.ForeignKey("Assets.id"))
    quantity = db.Column(db.Numeric(18, 6))
    avg_price = db.Column(db.Numeric(18, 2))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("Users", back_populates="holdings")
    assets = db.relationship("Assets", back_populates="holdings")


class Price_History(db.Model):
    __tablename__ = "Price_History"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    asset_id = db.Column(db.String(36), db.ForeignKey("Assets.id"))
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(18, 2))

    assets = db.relationship("Assets", back_populates="price_history")

class pwd(db.Model):
    __tablename__ = "pwd"

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    entity = db.Column(db.String(36), db.ForeignKey("Assets.id"))
    pwd = db.Column(db.Text, nullable=False)