import enum
import os
# Both spellings are bound on purpose. Generated code uses the trailing-
# underscore aliases so a modelled class named List, Optional or DateTime
# cannot shadow them. The PLAIN names are imported too because this file is
# routinely edited afterwards by an LLM, which writes ordinary Python and has
# no reason to know about the aliasing convention; without the plain names
# such edits fail to import:
#
#     Mapped_[Optional[int]]        undefined name 'Optional'
#     mapped_column(DateTime())     undefined name 'DateTime'
#
# so every aliased name below is bound both ways.
from typing import List, Optional, List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Enum, UniqueConstraint as _UniqueConstraint, event as _sa_event,
    Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, Interval,
    PickleType, String, Table, Text, Time,
    Column as Column_, ForeignKey as ForeignKey_, Table as Table_,
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_,
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_,
    Interval as Interval_, PickleType as PickleType_,
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, Mapped as Mapped_, mapped_column,
    relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date, timedelta as dt_timedelta
from uuid import uuid4 as _uuid4


def _new_str_id() -> str:
    """Server-side surrogate for string primary keys named ``id``.

    A string PK has no autoincrement; without a default every INSERT dies
    on NOT NULL (the id is in nobody's hands: create schemas rightly
    exclude the server-owned ``id``, so the server must mint it).
    """
    return _uuid4().hex


def _configure_sqlite_engine(engine):
    """Enforce declared foreign keys on every SQLite connection."""
    if engine.dialect.name == "sqlite":
        @_sa_event.listens_for(engine, "connect")
        def _enable_foreign_keys(connection, _record):
            previous_autocommit = getattr(connection, "autocommit", None)
            if previous_autocommit is not None:
                connection.autocommit = True
            cursor = connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys=ON")
            finally:
                cursor.close()
                if previous_autocommit is not None:
                    connection.autocommit = previous_autocommit


class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class Frequency(enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class ResolutionStatus(enum.Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


# Tables definition for many-to-many relationships

# Tables definition
class User(Base):
    __tablename__ = "user"
    id: Mapped_[int] = mapped_column(primary_key=True)
    fullName: Mapped_[str] = mapped_column(String_(100))
    email: Mapped_[str] = mapped_column(String_(100))
    createdAt: Mapped_[dt_datetime] = mapped_column(DateTime_, default=dt_datetime.now)
    lastLoginAt: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True)

class SubGoal(Base):
    __tablename__ = "subgoal"
    id: Mapped_[int] = mapped_column(primary_key=True)
    title: Mapped_[str] = mapped_column(String_(100))
    description: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    createdAt: Mapped_[dt_datetime] = mapped_column(DateTime_, default=dt_datetime.now)
    targetDate: Mapped_[Optional_[dt_date]] = mapped_column(Date_, nullable=True)
    completed: Mapped_[bool] = mapped_column(Boolean_)
    parentResolution_id: Mapped_[int] = mapped_column(ForeignKey_("resolution.id"))

class Resolution(Base):
    __tablename__ = "resolution"
    id: Mapped_[int] = mapped_column(primary_key=True)
    title: Mapped_[str] = mapped_column(String_(100))
    description: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    createdAt: Mapped_[dt_datetime] = mapped_column(DateTime_, default=dt_datetime.now)
    updatedAt: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True, default=dt_datetime.now, onupdate=dt_datetime.now)
    targetDate: Mapped_[Optional_[dt_date]] = mapped_column(Date_, nullable=True)
    status: Mapped_[ResolutionStatus] = mapped_column(Enum(ResolutionStatus))
    category_id: Mapped_[int] = mapped_column(ForeignKey_("category.id"), nullable=True)
    owner_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class ProgressEntry(Base):
    __tablename__ = "progressentry"
    id: Mapped_[int] = mapped_column(primary_key=True)
    date: Mapped_[dt_datetime] = mapped_column(DateTime_)
    notes: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    amount: Mapped_[Optional_[float]] = mapped_column(Float_, nullable=True)
    author_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))
    habit_id: Mapped_[int] = mapped_column(ForeignKey_("habit.id"), nullable=True)
    resolution_id: Mapped_[int] = mapped_column(ForeignKey_("resolution.id"), nullable=True)

class Habit(Base):
    __tablename__ = "habit"
    id: Mapped_[int] = mapped_column(primary_key=True)
    name: Mapped_[str] = mapped_column(String_(100))
    description: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    createdAt: Mapped_[dt_datetime] = mapped_column(DateTime_, default=dt_datetime.now)
    frequency: Mapped_[Frequency] = mapped_column(Enum(Frequency))
    active: Mapped_[bool] = mapped_column(Boolean_)
    currentStreak: Mapped_[int] = mapped_column(Integer_)
    lastDoneAt: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True)
    habitUser_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class Category(Base):
    __tablename__ = "category"
    id: Mapped_[int] = mapped_column(primary_key=True)
    name: Mapped_[str] = mapped_column(String_(100))
    colorHex: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    createdAt: Mapped_[dt_datetime] = mapped_column(DateTime_, default=dt_datetime.now)


#--- Relationships of the user table
User.habits: Mapped_[List_["Habit"]] = relationship("Habit", back_populates="habitUser", foreign_keys=[Habit.habitUser_id], cascade="all, delete-orphan")
User.progressEntries: Mapped_[List_["ProgressEntry"]] = relationship("ProgressEntry", back_populates="author", foreign_keys=[ProgressEntry.author_id])
User.resolutions: Mapped_[List_["Resolution"]] = relationship("Resolution", back_populates="owner", foreign_keys=[Resolution.owner_id])

#--- Relationships of the subgoal table

SubGoal.parentResolution: Mapped_["Resolution"] = relationship("Resolution", back_populates="subGoals", uselist=False, foreign_keys=[SubGoal.parentResolution_id])

#--- Relationships of the resolution table

Resolution.category: Mapped_["Category"] = relationship("Category", back_populates="resolutions", uselist=False, foreign_keys=[Resolution.category_id])

Resolution.owner: Mapped_["User"] = relationship("User", back_populates="resolutions", uselist=False, foreign_keys=[Resolution.owner_id])
Resolution.progressEntries: Mapped_[List_["ProgressEntry"]] = relationship("ProgressEntry", back_populates="resolution", foreign_keys=[ProgressEntry.resolution_id])
Resolution.subGoals: Mapped_[List_["SubGoal"]] = relationship("SubGoal", back_populates="parentResolution", foreign_keys=[SubGoal.parentResolution_id], cascade="all, delete-orphan")

#--- Relationships of the progressentry table

ProgressEntry.author: Mapped_["User"] = relationship("User", back_populates="progressEntries", uselist=False, foreign_keys=[ProgressEntry.author_id])

ProgressEntry.habit: Mapped_["Habit"] = relationship("Habit", back_populates="progressEntries", uselist=False, foreign_keys=[ProgressEntry.habit_id])

ProgressEntry.resolution: Mapped_["Resolution"] = relationship("Resolution", back_populates="progressEntries", uselist=False, foreign_keys=[ProgressEntry.resolution_id])

#--- Relationships of the habit table

Habit.habitUser: Mapped_["User"] = relationship("User", back_populates="habits", uselist=False, foreign_keys=[Habit.habitUser_id])
Habit.progressEntries: Mapped_[List_["ProgressEntry"]] = relationship("ProgressEntry", back_populates="habit", foreign_keys=[ProgressEntry.habit_id])

#--- Relationships of the category table
Category.resolutions: Mapped_[List_["Resolution"]] = relationship("Resolution", back_populates="category", foreign_keys=[Resolution.category_id])

# Database connection (override the default with the DATABASE_URL environment variable)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")  # SQLite connection
engine = create_engine(DATABASE_URL)
_configure_sqlite_engine(engine)

if __name__ == "__main__":
    # Create tables in the database only when this module is executed directly,
    # so importing it never touches the database as a side effect.
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)  # folder for the default SQLite database
    Base.metadata.create_all(engine, checkfirst=True)