from app.models.model_mixin import ModelMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.db import db
from app.models.day import Day
from app.models.trip import Trip
from app.models.user import User

class Itinerary(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey('trip.id'), nullable=False)
    trip: Mapped["Trip"] = relationship("Trip", back_populates="itineraries")

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="itineraries")

    days: Mapped[list["Day"]] = relationship("Day", back_populates="itinerary")

    def to_dict(self):
        return dict(
            id=self.id,
            trip_id=self.trip_id,
            user_id=self.user_id
        )