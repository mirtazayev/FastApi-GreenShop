from enum import Enum

from fastapi import UploadFile, File
from pydantic import BaseModel, validator


class Category(str, Enum):
    house_plants = "house plants"
    potter_plants = "potter plants"
    seeds = "seeds"
    small_plants = "small plants"
    big_plants = "big plants"
    succulents = "succulents"
    trerrariums = "trerrariums"
    gardening = "gardening"
    accessories = "accessories"


class Size(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class FlowerDTO(BaseModel):
    title: str
    price: float
    image: UploadFile or None = File(None)
    description: str
    short_description: str
    tags: str
    in_stock: bool


class FlowerUpdateDTO(BaseModel):
    title: str
    price: str

    @validator("title")
    def valid_title(cls, v):
        if not v:
            raise ValueError('Title Cannot be null')
        if v.isspace():
            raise ValueError('Title Cannot be blank')
        return v.title()

    @validator("price")
    def valid_body(cls, v: str):
        if not v:
            raise ValueError('price Cannot be null')
        if v.isspace():
            raise ValueError('price cannot be blank')
        return v

    class Config:
        orm_mode = True
