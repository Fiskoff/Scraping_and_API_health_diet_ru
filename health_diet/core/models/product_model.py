from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    calories: Mapped[int] = mapped_column(Integer, default=0)
    protein: Mapped[float] = mapped_column(Float, default=0.0)
    fats: Mapped[float] = mapped_column(Float, default=0.0)
    carbs: Mapped[float] = mapped_column(Float, default=0.0)


