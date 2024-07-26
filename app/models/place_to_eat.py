from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, Text, ForeignKey
from app.db import db
from app.models.itinerary import Itinerary

class PlaceToEat(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    place: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    itinerary_id: Mapped[int] = mapped_column(ForeignKey('itinerary.id'), nullable=False)
    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="places_to_eat")

    def update_from_dict(self, data):
        self.place = data["place"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.description = data.get("description")
        self.itinerary_id = data["itinerary_id"]

    def to_dict(self):
        return dict(
            id=self.id,
            place=self.place,
            latitude=self.latitude,
            longitude=self.longitude,
            description=self.description,
            itinerary_id=self.itinerary_id
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            place=data["place"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            description=data.get("description"),
            itinerary_id=data["itinerary_id"]
        )
