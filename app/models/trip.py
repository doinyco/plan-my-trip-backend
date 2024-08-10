from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float
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
    description: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="trips")

    place_to_rest: Mapped["PlaceToRest"] = relationship("PlaceToRest", back_populates="trip")

    itineraries: Mapped[list["Itinerary"]] = relationship(
        "Itinerary", 
        back_populates="trip",
        cascade="all, delete-orphan"
        )

    def update_from_dict(self, data):
        self.destination = data["destination"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.budget = data["budget"]
        self.description = data["description"]

    def to_dict(self):
        data = dict(
            id=self.id,
            destination=self.destination,
            latitude=self.latitude,
            longitude=self.longitude,
            start_date=self.start_date,
            end_date=self.end_date,
            budget=self.budget,
            description=self.description,
            itineraries=[itinerary.to_dict() for itinerary in self.itineraries]
        )

        if self.user_id:
            data["user_id"] = self.user_id

        if self.place_to_rest:
            data["place_to_rest"] = self.place_to_rest.to_dict()
        
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
            description=data["description"],
            user_id=data["user_id"]
        )