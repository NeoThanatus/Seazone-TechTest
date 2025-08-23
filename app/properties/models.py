from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from app.reservations.models import Reservations


class Base(DeclarativeBase):
    pass


class Properties(Base):
    __tablename__ = "properties"

    property_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_street: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_number: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_neighborhood: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_city: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_state: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    rooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    price_per_night: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    reservations: Mapped[list["Reservations"]] = relationship(
        back_populates="property")
