from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, Text, ForeignKey
from app.db import db
from app.models.trip import Trip

class PlaceToRest(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    place: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey('trip.id'), nullable=True)
    trip: Mapped["Trip"] = relationship(back_populates="place_to_rest")

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
