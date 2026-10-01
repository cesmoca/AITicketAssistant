from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..persistence.sqlalchemy_base import SQLAlchemyBase


class TicketEntity(SQLAlchemyBase):
    
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    appliance: Mapped[str | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(nullable=True)
    failure: Mapped[str | None] = mapped_column(nullable=True)
    other_details: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)