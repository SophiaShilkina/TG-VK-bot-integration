from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UsersBase(Base):
    __tablename__ = "users"

    userId: Mapped[int] = mapped_column(primary_key=True, index=True)
    act: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    dates: Mapped[str] = mapped_column(String, nullable=True)
    persons: Mapped[str] = mapped_column(String, nullable=True)
    genders: Mapped[str] = mapped_column(String, nullable=True)
    rooms: Mapped[str] = mapped_column(String, nullable=True)
    pastRooms: Mapped[str] = mapped_column(String, nullable=True)
