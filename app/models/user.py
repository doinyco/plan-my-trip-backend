from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from ..db import db
from .model_mixin import ModelMixin


class User(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    trips: Mapped[list["Trip"]] = relationship(back_populates="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_from_dict(self, data):
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email
        )
    
    @classmethod
    def from_dict(cls, data):
        return User(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )