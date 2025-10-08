from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, ForeignKey, CheckConstraint, Text, DECIMAL, TIMESTAMP, Time, text, Index, Table, ForeignKeyConstraint
from app.config.database import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
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
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
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

    restaurants: Mapped[List['Restaurants']] = relationship('Restaurant', uselist=True, back_populates='address')

class Cuisines(Base):
    __tablename__ = 'cuisines'
    __table_args__ = (
        Index('cuisine_name', 'cuisine_name', unique=True),
    )

    id = mapped_column(Integer , primary_key=True)
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
    user_id = mapped_column(Integer, nullable=False)
    cuisine_id = mapped_column(Integer, nullable=False)
    address_id = mapped_column(Integer, nullable=False)
    restaurant_name = mapped_column(String(200), nullable=False)
    tel_number = mapped_column(String(20), nullable=False)
    description = mapped_column(Text, nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text('current_timestamp()'))
    pickup_time = mapped_column(DateTime, nullable=False)
    image_url = mapped_column(String(255))
    is_active = mapped_column(Integer, server_default=text('0'))

    address: Mapped['Addresses'] = relationship('Address', back_populates='restaurants')
    cuisine: Mapped['Cuisines'] = relationship('Cuisine', back_populates='restaurants')
    user: Mapped['User'] = relationship('User', back_populates='restaurants')
    foods: Mapped[List['Foods']] = relationship('Food', uselist=True, back_populates='restaurant')
    
class Foods(Base):
    __tablename__ = 'foods'
    __table_args__ = (
        ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
    )

    id = mapped_column(Integer, primary_key=True)
    food_name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)
    restaurant_id = mapped_column(Integer, nullable=False)
    price = mapped_column(DECIMAL(10, 2), nullable=False)
    initial_stock = mapped_column(Integer, nullable=False)
    preparation_time = mapped_column(Time, nullable=False)
    image_url = mapped_column(String(255))

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

    id = mapped_column(Integer, primary_key=True)
    cat_name = mapped_column(String(100), nullable=False)

    foods: Mapped[List['Foods']] = relationship('Food', secondary='foodcats', back_populates='categories')
