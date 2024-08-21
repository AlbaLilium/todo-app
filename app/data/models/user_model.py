from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.db_connection import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20), nullable=True)
    username: Mapped[str] = mapped_column(String(10), unique=True)
    password: Mapped[str] = mapped_column(String(150))
