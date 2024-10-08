from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, Text, ForeignKey
from app.db import db

class PlaceToEat(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    place: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    day_id: Mapped[int] = mapped_column(ForeignKey('day.id'), nullable=False)
    day: Mapped["Day"] = relationship("Day", back_populates="places_to_eat")

    def update_from_dict(self, data):
        self.place = data["place"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.description = data.get("description")

    def to_dict(self):
        return dict(
            id=self.id,
            place=self.place,
            latitude=self.latitude,
            longitude=self.longitude,
            description=self.description
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            place=data["place"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            description=data.get("description")
        )
