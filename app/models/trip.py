from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional

from app.models.user import User
from ..db import db
from .model_mixin import ModelMixin


class Trip(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    destination: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    budget: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="trips")

    def update_from_dict(self, data):
        self.destination = data["destination"]
        self.dates = data["dates"]
        self.bugdet = data["bugdet"]

    def to_dict(self):
        data = dict(
            id=self.id,
            destination=self.destination,
            dates=self.dates,
            budget=self.budget
        )

        if self.user_id:
            data["user_id"] = self.user_id
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        return Trip(
            destination=data["destination"],
            dates=data["dates"],
            budget=data["budget"]
        )