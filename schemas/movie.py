from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=30, max_length=35)
    year: int = Field(ge=1906, le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Movie name",
                "overview": "Overview Overview Overview Overview",
                "year": 2023,
                "rating": 10,
                "category": "Drama"
            }
        }
