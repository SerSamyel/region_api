from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import Base, session
from flask_jwt_extended import create_access_token
from datetime import timedelta
import bcrypt


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    relation_id = relationship('Town', backref='region', lazy=True)

    def _init__(self, name):
        self.name = name



class Town(Base):
    __tablename__ = 'town'

    id = Column(Integer, primary_key=True)
    town_name = Column(String(50), nullable=False)

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    def __init__(self, town_name, region_id):
        self.town_name = town_name
        self.region_id = region_id

    def __repr__(self):
        return f"{self.id=} { self.town_name=} {self.region_id=}"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())

    def __repr__(self):
        return f"{self.id=} {self.name=} {self.email=} {self.password=}"

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = session.query(cls).filter(cls.email == email).first()
        if not bcrypt.checkpw(password.encode('utf-8'), user.password):
            raise Exception("No user with this password")
        return user