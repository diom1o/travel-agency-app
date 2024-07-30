import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    bookings = relationship('Booking', back_populates='user')
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

class Tour(Base):
    __tablename__ = 'tours'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    bookings = relationship('Booking', back_populates='tour')
    
    def __repr__(self):
        return f"<Tour(title={self.title}, price={self.price})>"

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    tour_id = Column(Integer, ForeignKey('tours.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    booking_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, default=1)
    tour = relationship('Tour', back_populates='bookings')
    user = relationship('User', back_populates='bookings')
    
    def __repr__(self):
        return f"<Booking(tour_id={self.tour_id}, user_id={self.user_id}, booking_date={self.booking_date})>"

Base.metadata.create_all(engine)