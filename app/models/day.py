from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.db import db

class Day(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    itinerary_id: Mapped[int] = mapped_column(ForeignKey('itinerary.id'), nullable=False)
    # activities: Mapped[list["Activity"]] = relationship("Activity", back_populates="day")

    def update_from_dict(self, data):
        self.day_number = data.get("day_number", self.day_number)
        self.itinerary_id = data.get("itinerary_id", self.itinerary_id)

    def to_dict(self):
        return dict(
            id=self.id,
            day_number=self.day_number,
            itinerary_id=self.itinerary_id
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            day_number=data.get("day_number"),
            itinerary_id=data.get("itinerary_id")
        )
