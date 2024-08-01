from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float
from typing import Optional
from ..db import db
from .model_mixin import ModelMixin

class Trip(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    destination: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    budget: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="trips")

    itineraries: Mapped[list["Itinerary"]] = relationship("Itinerary", back_populates="trip")

    def update_from_dict(self, data):
        self.destination = data["destination"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.budget = data["budget"]

    def to_dict(self):
        data = dict(
            id=self.id,
            destination=self.destination,
            latitude=self.latitude,
            longitude=self.longitude,
            start_date=self.start_date,
            end_date=self.end_date,
            budget=self.budget
        )

        if self.user_id:
            data["user_id"] = self.user_id
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        return Trip(
            destination=data["destination"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            start_date = data["start_date"],
            end_date = data["end_date"],
            budget=data["budget"],
            user_id=data["user_id"]
        )