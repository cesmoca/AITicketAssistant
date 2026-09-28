from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer
from ..persistence.sqlalchemy_base import SQLAlchemyBase
from ..domain.task import Task

class TaskEntity(SQLAlchemyBase):
    
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    appliance: Mapped[str | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(nullable=True)
    failure: Mapped[str | None] = mapped_column(nullable=True)
    task_type: Mapped[str] = mapped_column(nullable=True)