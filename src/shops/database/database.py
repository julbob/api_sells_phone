"""
This module contains all function to interact with the Database PostgreSQL.
"""
import os
import re
from typing import Any, List
from sqlalchemy import (
    Engine,
    MetaData,
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Mapped, Session

# Engine for PostgreSQL

USERNAME_DB: str = os.environ.get("USERNAME_DB", "admin")
PASSWORD_DB: str = os.environ.get("PASSWORD_DB", "admin")
engine: Engine = create_engine(
    f"postgresql://{USERNAME_DB}:{PASSWORD_DB}@localhost/product"
)
metadata: MetaData = MetaData()
Base = declarative_base()


class Product(Base):
    """Products table

    id: Integer, primary key, auto increment
    name: String, name of product
    average_price: Numeric, Average price of product. Automatic compute
    sells: List of sells of product"""

    __tablename__: str = "products"
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(255))
    average_price: Column = Column(Numeric)
    sells: Mapped[List["Sell"]] = relationship(
        "Sell", cascade="all, delete", back_populates="product"
    )

    def to_dict(self):
        """Return dict for Product with its sells"""
        return {
            "id": self.id,
            "name": self.name,
            "sells": [sell.to_dict_without_product() for sell in self.sells],
        }

    def to_dict_without_sells(self):
        """Return dict for Product without its sells"""
        return {"id": self.id, "name": self.name, "average_price": self.average_price}

    def update_line(self, data: Any):
        """Update line in table Product"""
        keys: List[str] = data.keys()
        if "name" in keys:
            self.name = re.sub(r"\s+", " ", data["name"]).strip().lower()


class Sell(Base):
    """Sells table

    id: Integer, primary key, auto increment
    shop: String, name of shop
    product_id: Integer, id of product
    sell_date: Date, date of sell
    price: Numeric, price of product
    product: Product: full information of product"""

    __tablename__: str = "sells"
    id: Column = Column(Integer, primary_key=True)
    shop: Column = Column(String(255))
    product_id: Column = Column(Integer, ForeignKey("products.id"))
    sell_date: Column = Column(Date)
    price: Column = Column(Numeric)
    product: Mapped["Product"] = relationship("Product", back_populates="sells")

    def to_dict(self):
        """Return dict for Sell with its product"""
        return {
            "id": self.id,
            "shop": self.shop,
            "product_id": self.product_id,
            "sell_date": self.sell_date.strftime("%Y-%m-%d"),
            "price": self.price,
            "product": self.product.to_dict_without_sells(),
        }

    def to_dict_without_product(self):
        """Return dict for Sell without product"""
        return {
            "id": self.id,
            "shop": self.shop,
            "product_id": self.product_id,
            "sell_date": self.sell_date.strftime("%Y-%m-%d"),
            "price": self.price,
        }

    def update_line(self, data: Any):
        """Update line in table Sells"""
        keys: List[str] = data.keys()
        if "shop" in keys:
            self.shop = re.sub(r"\s+", " ", data["shop"]).strip().lower()
        if "product_id" in keys:
            self.product_id = data["product_id"]
        if "sell_date" in keys:
            self.sell_date = data["sell_date"]
        if "price" in keys:
            self.price = data["price"]


# Create Session
sessionmake: sessionmaker = sessionmaker(bind=engine)
session: Session = sessionmake()
