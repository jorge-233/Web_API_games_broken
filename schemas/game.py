from pydantic import BaseModel, Field


class GameCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    genre: str = Field(min_length=3, max_length=40)
    platform: str = Field(min_length=2, max_length=30)

    # CORREGIDO: el límite inferior era ge=0 y aceptaba stock 0.
    # Ahora es ge=1, así que stock 0 se rechaza con 422.
    stock: int = Field(ge=1, le=50)

    active: bool = True


class GameResponse(BaseModel):
    id: int
    title: str
    genre: str
    platform: str
    stock: int
    active: bool