import datetime
from pydantic import BaseModel


class CitySchemaBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CitySchemaDetail(CitySchemaBase):
    id: int

class TemperatureSchema(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True
