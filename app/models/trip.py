from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Date, ForeignKey
from app.db import db
from app.models.user import User

class Trip(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    latitudeDestination: Mapped[float] = mapped_column(Float, nullable=False)
    longitudeDestination: Mapped[float] = mapped_column(Float, nullable=False)
    startDate: Mapped[Date] = mapped_column(Date, nullable=False)
    endDate: Mapped[Date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="trips")
    
    itinerary = relationship("Itinerary", back_populates="trip")


    def update_from_dict(self, data):
        self.destination = data["destination"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.budget = data["budget"]
        # Latitude and longitude might be provided
        self.latitude_destination = data.get("latitude_destination", self.latitude_destination)
        self.longitude_destination = data.get("longitude_destination", self.longitude_destination)
        self.user_id = data.get("user_id", self.user_id)

    def to_dict(self):
        data = {
            "id": self.id,
            "destination": self.destination,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "latitude_destination": self.latitude_destination,
            "longitude_destination": self.longitude_destination
        }
        
        if self.user_id is not None:
            data["user_id"] = self.user_id
        
        return data

    
    @classmethod
    def from_dict(cls, data):
        return cls(
            destination=data["destination"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            budget=data["budget"],
            latitude_destination=data.get("latitude_destination"),  # Use get for optional fields
            longitude_destination=data.get("longitude_destination"), 
            user_id=data.get("user_id")  # Use get for optional fields
        )

    
    def update_trip_with_coordinates(self, latitude: float, longitude: float):
        self.latitude_destination = latitude
        self.longitude_destination = longitude
        db.session.commit()
