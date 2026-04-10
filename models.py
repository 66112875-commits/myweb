from sqlalchemy import Column, Integer, String , Float , ForeignKey , DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    role_id = Column(Integer, nullable=False)
    role_name = Column(String(100), nullable=False)

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=True)
    tax_id = Column(String(15), nullable=True)

class Orders(Base):
    __tablename__ = "orderss"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), nullable=False)
    order_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")
    amount_untaxed = Column(Float, nullable=True)
    amount_tax = Column(Float, nullable=True)
    amount_total = Column(Float, nullable=True)
    state = Column(String(50), nullable=True)

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order")

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product")

    qty = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_no = Column(String(50))
    order_date = Column(DateTime)
    amount_total = Column(Float)
    state = Column(String(50))  # Draft, Paid, Cancel
