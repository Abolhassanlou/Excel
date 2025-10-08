from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, ForeignKey, CheckConstraint, Text, DECIMAL, TIMESTAMP, Time, text, Index, Table, ForeignKeyConstraint
from app.config.database import Base
from sqlalchemy.orm import relationship, Mapped
from typing import List

metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('role IN (0,1,2)', name='check_user_role'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Integer, default=0)  # Role: 0 = default, 1 = seller, 2 = admin
    name = Column(String(150))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    tokens = relationship("UserToken", back_populates="user")
    restaurants: Mapped[List['Restaurants']] = relationship('Restaurant', uselist=True, back_populates='user')

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")

class Addresses(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)
    flat_number = Column(String(20))
    door_number = Column(String(20))
    google_maps_link = Column(String(255))

    restaurants: Mapped[List['Restaurants']] = relationship('Restaurant', uselist=True, back_populates='address')

class Cuisines(Base):
    __tablename__ = 'cuisines'
    __table_args__ = (
        Index('cuisine_name', 'cuisine_name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    cuisine_name = Column(String(100), nullable=False)

    restaurants: Mapped[List['Restaurants']] = relationship('Restaurants', uselist=True, back_populates='cuisine')

class Restaurants(Base):
    __tablename__ = 'restaurants'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['addresses.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['cuisine_id'], ['cuisines.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    cuisine_id = Column(Integer, nullable=False)
    address_id = Column(Integer, nullable=False)
    restaurant_name = Column(String(200), nullable=False)
    tel_number = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    pickup_time = Column(DateTime, nullable=False)
    image_url = Column(String(255))
    is_active = Column(Integer, server_default=text('0'))

    address: Mapped['Addresses'] = relationship('Address', back_populates='restaurants')
    cuisine: Mapped['Cuisines'] = relationship('Cuisine', back_populates='restaurants')
    user: Mapped['User'] = relationship('User', back_populates='restaurants')
    foods: Mapped[List['Foods']] = relationship('Food', uselist=True, back_populates='restaurant')
    
class Foods(Base):
    __tablename__ = 'foods'
    __table_args__ = (
        ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
    )

    id = Column(Integer, primary_key=True)
    food_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    initial_stock = Column(Integer, nullable=False)
    preparation_time = Column(Time, nullable=False)
    image_url = Column(String(255))

    categories: Mapped[List['Categories']] = relationship('Category', secondary='foodcats', back_populates='foods')
    restaurant: Mapped['Restaurants'] = relationship('Restaurant', back_populates='foods')

t_foodcats = Table(
    'foodcats', metadata,
    Column('food_id', Integer, primary_key=True, nullable=False),
    Column('category_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
)

class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        Index('cat_name', 'cat_name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    cat_name = Column(String(100), nullable=False)

    foods: Mapped[List['Foods']] = relationship('Food', secondary='foodcats', back_populates='categories')
