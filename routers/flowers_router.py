import shutil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database_config import get_db
from models.main import Flowers
from schema.flower_DTO import FlowerDTO, Category, Size
from services import flowers_service

router = APIRouter(tags=['Flowers Router'], prefix="/flowers")


@router.post('/flowers-create')
def create_flower(dto: FlowerDTO = Depends(), category: Category = Category.house_plants, size: Size = Size.small,
                  db: Session = Depends(get_db)):
    return flowers_service.create(dto=dto, db=db, category=category, size=size)


@router.get("")
def get_flowers(db: Session = Depends(get_db)):
    flowers = db.query(Flowers).all()
    return {'flowers': flowers}


@router.get("/{flower_id}")
def get_flower_by_id(flower_id: int, db: Session = Depends(get_db)):
    flowers = db.query(Flowers).all()
    for flower in flowers:
        if flower.id == flower_id:
            return flower
    return {'status': f"Flower not found with id : {flower_id}"}


@router.put("/flowers-update/{flower_id}")
def update_flower(
        flower_id: int,
        dto: FlowerDTO = Depends(),
        db: Session = Depends(get_db)
):
    data = FlowerDTO(**dto.__dict__).dict(exclude_unset=True)
    if not db.query(Flowers).filter(Flowers.id == flower_id).first():
        return {"error": f"Flower is not found by id: {flower_id}"}
    else:
        if len(dto.image.filename):
            file_url = 'media/flowers/' + dto.image.filename
            with open(file_url, "wb") as buffer:
                shutil.copyfileobj(dto.image.file, buffer)
            data.update({'image': file_url})
        db.query(Flowers).filter(Flowers.id == flower_id).update(data)
        db.commit()
        return f'Flowers is updated successfully'


@router.delete("/flowers-delete/{flower_id}")
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    flowers = db.query(Flowers).all()
    for flower in flowers:
        if flower.id == flower_id:
            db.delete(flower)
            db.commit()
            return {'status': 'Flower is deleted'}
    else:
        raise HTTPException(status_code=404, detail=f"Flower is not found with id : {flower_id}")
