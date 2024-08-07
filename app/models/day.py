from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.db import db
from app.models.activity import Activity
from app.models.place_to_eat import PlaceToEat
from app.models.place_to_rest import PlaceToRest

class Day(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)

    itinerary_id: Mapped[int] = mapped_column(ForeignKey('itinerary.id'), nullable=False)
    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="days")

    activities: Mapped[list["Activity"]] = relationship(
        "Activity", 
        back_populates="day",
        cascade="all, delete-orphan")
    places_to_eat: Mapped[list["PlaceToEat"]] = relationship(
        "PlaceToEat", 
        back_populates="day",
        cascade="all, delete-orphan"
        )
    places_to_rest: Mapped[list["PlaceToRest"]] = relationship(
        "PlaceToRest", 
        back_populates="day",
        cascade="all, delete-orphan"
        )

    def update_from_dict(self, data):
        self.day_number = data.get("day_number", self.day_number)
        self.itinerary_id = data.get("itinerary_id", self.itinerary_id)

    def to_dict(self):
        return dict(
            id=self.id,
            day_number=self.day_number,
            itinerary_id=self.itinerary_id,
            activities=[activity.to_dict() for activity in self.activities],
            places_to_eat=[place_to_eat.to_dict() for place_to_eat in self.places_to_eat],
            places_to_rest=[place_to_rest.to_dict() for place_to_rest in self.places_to_rest]
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            day_number=data.get("day_number"),
            itinerary_id=data.get("itinerary_id")
        )
