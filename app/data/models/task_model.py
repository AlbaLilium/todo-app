from sqlalchemy import String, Enum, ForeignKey, Integer
from app.db.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.data.enum import TaskStatusEnum


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(15))
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status = mapped_column(Enum(*[e.value for e in TaskStatusEnum]), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
