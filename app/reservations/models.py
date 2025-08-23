from datetime import date
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ..db import Base


class Reservations(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    client_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    guest_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_value: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.property_id"),
        nullable=False
    )

    property: Mapped["Properties"] = relationship(
        back_populates="reservations"
    )
