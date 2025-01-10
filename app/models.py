import datetime
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, BigInteger

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(primary_key = True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    store_name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)

    # Establishing a relationship with the Prices table
    prices: Mapped[List["Price"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    
    # Establishing a relationship with the Users table
    user: Mapped["User"] = relationship(back_populates="products")

    def __repr__(self):
        return f"""<Product(product_id={self.product_id}, product_name='{self.product_name}', store_name='{self.store_name}
    , url={self.url}, tg_id={self.tg_id}, prices={self.prices}')>"""


class Price(Base):
    __tablename__ = 'prices'

    price_id: Mapped[int] = mapped_column(primary_key = True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=True) # Валюта
    discount: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # Знижка
    unit_of_measure: Mapped[str] = mapped_column(String(100), default='шт.', nullable=True) # Одиниця виміру
    status: Mapped[str] = mapped_column(String(100), default=None, nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)

    # Establishing a relationship with the Products table
    product: Mapped["Product"] = relationship(back_populates="prices")

    def __repr__(self):
        return f"""<Price(price_id={self.price_id}, product_id={self.product_id}, price={self.price}, currency={self.currency}
    , discount={self.discount}, unit_of_measure={self.unit_of_measure}, date={self.date})>"""
    
    
    
class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger ,primary_key=True)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Establishing a relationship with the Products table
    products: Mapped[List["Product"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(tg_id={self.tg_id}, user_name='{self.user_name}')>"

