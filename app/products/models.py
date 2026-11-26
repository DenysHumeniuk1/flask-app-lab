from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="category", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Category {self.name!r}>"


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", name="fk_products_category_id_categories"),
        nullable=True,
    )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="1"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )

    category: Mapped[Category | None] = relationship(
        back_populates="products"
    )

    def __repr__(self) -> str:
        return f"<Product {self.name!r} ({self.price})>"
