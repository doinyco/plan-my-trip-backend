from app.models.activity import Activity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.db import db
from app.models.itinerary import Itinerary
from app.models.model_mixin import ModelMixin


class Day(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    itinerary_id: Mapped[int] = mapped_column(ForeignKey('itinerary.id'), nullable=False)
    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="days")

    activities: Mapped["Activity"] = relationship("Activity", back_populates="day")

    def update_from_dict(self, data):
        self.day_number = data.get("day_number", self.day_number)

    def to_dict(self):
        return dict(
            id=self.id,
            day_number=self.day_number,
            trip_id=self.trip_id
        )

    @classmethod
    def from_dict(cls, data):
        return Day(
            day_number=data.get("day_number"),
            trip_id=data.get("trip_id")
        )