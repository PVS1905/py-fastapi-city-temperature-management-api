from typing import Annotated
from fastapi import APIRouter
from datetime import datetime
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.orm import Session
from city import schemas, crud, models
from city.crud import fetch_temperature
from database.deps import get_db

city_router = APIRouter()

@city_router.get("/cities/", response_model=list[schemas.CitySchemaDetail])
def get_cities(
    db: Annotated[Session, Depends(get_db)],
    limit: int | None = None,
):
    return crud.get_city(db=db, limit=limit)


@city_router.post("/city/", response_model=schemas.CitySchemaDetail)
def create_city(
    city: schemas.CitySchemaBase,
    db: Session = Depends(get_db),

):
    return crud.create_city(db=db, city=city)


@city_router.get("/city/{city_id}/", response_model=schemas.CitySchemaDetail)
def get_city(
    db: Annotated[Session, Depends(get_db)],
    city_id: int,
):
    return crud.get_city_by_id(db=db, city_id=city_id)


@city_router.put("/city/{city_id}/", response_model=schemas.CitySchemaDetail)
def get_city(
    db: Annotated[Session, Depends(get_db)],
    city_id: int,
    city: schemas.CitySchemaBase
):
    return crud.city_update(db=db, city_id=city_id, city=city)


@city_router.delete("/city/{city_id}/", status_code=204)
def get_city(
    db: Annotated[Session, Depends(get_db)],
    city_id: int,
):
    return crud.city_delete(db=db, city_id=city_id)


@city_router.post("/temperatures/update")
async def temperatures_update(db: Session = Depends(get_db)):
    cities = db.scalars(select(models.City)).all()

    for city in cities:
        temp = await fetch_temperature(city.name)

        db_temp = models.Temperature(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temp
        )

        db.add(db_temp)

    db.commit()

    return {"message": "Temperatures updated"}


@city_router.get("/temperatures", response_model=list[schemas.TemperatureSchema])
def get_temperatures(db: Session = Depends(get_db)):
    return db.scalars(select(models.Temperature)).all()


@city_router.get("/temperatures/", response_model=list[schemas.TemperatureSchema])
def get_temperatures_by_city(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    return db.scalars(query).all()
