from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Text
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Users(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250),nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    query: Mapped[str] = mapped_column(Text(1000), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    def __str__(self) -> str:
        return f"User ID: {self.id}, Name: {self.first_name}, Email: {self.email}"