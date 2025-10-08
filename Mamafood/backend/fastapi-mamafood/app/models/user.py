from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, func, ForeignKey, 
    Index, ForeignKeyConstraint, Text, TIMESTAMP, text , Time , DECIMAL , Table
)
from app.config.database import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped 
from typing import List

metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150))
    role = mapped_column(Integer, default=0)  # 0 = default, 1 = seller, 2 = admin
    email = mapped_column(String(255), unique=True, index=True)
    password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=False)
    verified_at = mapped_column(DateTime, nullable=True, default=None)
    updated_at = mapped_column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    tokens = relationship("UserToken", back_populates="user")
    restaurants: Mapped[List['Restaurants']] = relationship('Restaurants', uselist=True, back_populates='user')

    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()

class UserToken(Base):
    __tablename__ = "user_tokens"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = mapped_column(String(250), nullable=True, index=True, default=None)
    refresh_key = mapped_column(String(250), nullable=True, index=True, default=None)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    expires_at = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")

class Addresses(Base):
    __tablename__ = 'addresses'

    id = mapped_column(Integer, primary_key=True)
    street = mapped_column(String(100), nullable=False)
    city = mapped_column(String(50), nullable=False)
    postal_code = mapped_column(String(20), nullable=False)
    flat_number = mapped_column(String(20))
    door_number = mapped_column(String(20))
    google_maps_link = mapped_column(String(255))

    restaurants: Mapped[List['Restaurants']] = relationship('Restaurants', uselist=True, back_populates='address')

class Cuisines(Base):
    __tablename__ = 'cuisines'
    __table_args__ = (Index('cuisine_name', 'cuisine_name', unique=True),)

    id = mapped_column(Integer, primary_key=True)
    cuisine_name = mapped_column(String(100), nullable=False)

    restaurants: Mapped[List['Restaurants']] = relationship('Restaurants', uselist=True, back_populates='cuisine')

class Restaurants(Base):
    __tablename__ = 'restaurants'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['addresses.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['cuisine_id'], ['cuisines.id'], ondelete='CASCADE'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    cuisine_id = mapped_column(Integer, ForeignKey('cuisines.id'), nullable=False)
    address_id = mapped_column(Integer, ForeignKey('addresses.id'), nullable=False)
    restaurant_name = mapped_column(String(200), nullable=False)
    tel_number = mapped_column(String(20), nullable=False)
    description = mapped_column(Text, nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    pickup_time = mapped_column(String(5), nullable=False)  # Store as string (HH:MM format)
    image_url = mapped_column(String(255))
    is_active = mapped_column(Integer, server_default=text('0'))

    address: Mapped['Addresses'] = relationship('Addresses', back_populates='restaurants')
    cuisine: Mapped['Cuisines'] = relationship('Cuisines', back_populates='restaurants')
    user: Mapped['User'] = relationship('User', back_populates='restaurants')

    foods: Mapped[List['Foods']] = relationship('Foods', uselist=True, back_populates='restaurant' , lazy='dynamic')

class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)

    foods: Mapped[List['Foods']] = relationship('Foods', secondary='foodcats', back_populates='categories')

    
class Foods(Base):
    __tablename__ = 'foods'
    __table_args__ = (
        ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)
    restaurant_id = mapped_column(Integer, nullable=False)
    price = mapped_column(DECIMAL(10, 2), nullable=False)
    initial_stock = mapped_column(Integer, nullable=False)
    preparation_time = mapped_column(Time, nullable=False)
    image_url = mapped_column(String(255))

    categories: Mapped[List['Categories']] = relationship('Categories', secondary='foodcats', back_populates='foods')
    restaurant: Mapped['Restaurants'] = relationship('Restaurants', back_populates='foods')

    @property
    def cuisine_id(self):
        return self.restaurant.cuisine_id
    
t_foodcats = Table(
    'foodcats', metadata,
    Column('food_id', Integer, primary_key=True, nullable=False),
    Column('category_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
    
)

