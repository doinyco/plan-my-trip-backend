from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, Text, ForeignKey
from app.db import db
from app.models.day import Day

class Activity(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    day_id: Mapped[int] = mapped_column(ForeignKey('day.id'), nullable=False)
    day: Mapped["Day"] = relationship("Day", back_populates="activities")

    def update_from_dict(self, data):
        self.activity = data["activity"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.description = data.get("description")
        self.day_id = data["day_id"]

    def to_dict(self):
        return dict(
            id=self.id,
            activity=self.activity,
            latitude=self.latitude,
            longitude=self.longitude,
            description=self.description,
            day_id=self.day_id
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            activity=data["activity"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            description=data.get("description"),
            day_id=data["day_id"]
        )
