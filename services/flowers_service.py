import shutil

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from models.main import Flowers
from schema.flower_DTO import FlowerDTO


def create(dto: FlowerDTO, db: Session, category, size):
    data = dto.dict()
    flower = Flowers(**data)
    if len(dto.image.filename):
        file_url = 'media/flowers/' + dto.image.filename
        with open(file_url, "wb") as buffer:
            shutil.copyfileobj(dto.image.file, buffer)
        data.update({'image': file_url})
        flower = Flowers(**data)
        flower.category = category
        flower.size = size
        db.add(flower)
        db.commit()
        db.refresh(flower)
    return flower


def get(flower_id: int, db: Session):
    flower = db.query(Flowers).filter(Flowers.id == flower_id).first()
    if not flower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Flower is not found with id : '{flower_id}'")
    return flower
