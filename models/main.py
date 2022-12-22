import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, Boolean, Float

from database.database_config import Base
from models.shared.base_models import BaseModel


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class Users(BaseModel, Base):
    __tablename__ = 'user'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    username: str = Column(String(100), index=False)
    password: str = Column(String(300))
    email: str = Column(String(300))
    is_active: bool = Column(Boolean, server_default='True')


class Flowers(BaseModel, Base):
    __tablename__ = 'flower'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    title: str = Column(String(255))
    price: float = Column(Float)
    short_description: str = Column(String(255))
    description: str = Column(String(1000))
    tags: str = Column(String(100))
    category: str = Column(String(255))
    image: str = Column(String(255))
    size: str = Column(
        ChoiceType({"small": "small", "medium": "medium", "large": "large"}), nullable=False
    )
    in_stock: bool = Column(Boolean, server_default='True')
