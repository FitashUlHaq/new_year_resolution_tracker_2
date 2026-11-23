import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db, integrity_error_detail
from bal_stdlib import *

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/habit/", response_model=None, tags=["Habit"])
def get_all_habit(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Habit)
        query = query.options(joinedload(Habit.habitUser))
        habit_list = query.all()

        # Serialize with relationships included
        result = []
        for db_habit in habit_list:
            item_dict = db_habit.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if db_habit.habitUser:
                related_obj = db_habit.habitUser
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['habitUser'] = related_dict
            else:
                item_dict['habitUser'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            related_progressentry_list = database.query(ProgressEntry).filter(ProgressEntry.habit_id == db_habit.id).all()
            item_dict['progressEntries'] = []
            for related_progressentry_obj in related_progressentry_list:
                related_progressentry_dict = related_progressentry_obj.__dict__.copy()
                related_progressentry_dict.pop('_sa_instance_state', None)
                item_dict['progressEntries'].append(related_progressentry_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Habit).all()


@router.get("/habit/count/", response_model=None, tags=["Habit"])
def get_count_habit(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Habit entities"""
    count = database.query(Habit).count()
    return {"count": count}


@router.get("/habit/paginated/", response_model=None, tags=["Habit"])
def get_paginated_habit(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Habit entities"""
    total = database.query(Habit).count()
    habit_list = database.query(Habit).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": habit_list
        }

    result = []
    for db_habit in habit_list:
        progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.habit_id == db_habit.id).all()
        item_data = {
            "habit": db_habit,
            "progressEntries_ids": [x[0] for x in progressEntries_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/habit/search/", response_model=None, tags=["Habit"])
def search_habit(
    active: bool = None,
    currentStreak: int = None,
    description: str = None,
    name: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Habit entities by attributes"""
    query = database.query(Habit)

    if active is not None:
        query = query.filter(Habit.active == active)
    if currentStreak is not None:
        query = query.filter(Habit.currentStreak == currentStreak)
    if description is not None:
        query = query.filter(Habit.description.ilike(f"%{description}%"))
    if name is not None:
        query = query.filter(Habit.name.ilike(f"%{name}%"))

    results = query.all()
    return results


@router.get("/habit/{habit_id}/", response_model=None, tags=["Habit"])
async def get_habit(habit_id: int, database: Session = Depends(get_db)) -> Habit:
    db_habit = database.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.habit_id == db_habit.id).all()
    response_data = {
        "habit": db_habit,
        "progressEntries_ids": [x[0] for x in progressEntries_ids]}
    return response_data



@router.post("/habit/", response_model=None, tags=["Habit"])
async def create_habit(habit_data: HabitCreate, database: Session = Depends(get_db)) -> Habit:

    if habit_data.habitUser is not None:
        related_habitUser = database.query(User).filter(User.id == habit_data.habitUser).first()
        if not related_habitUser:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_habit = Habit(
        active=habit_data.active,        currentStreak=habit_data.currentStreak,        description=habit_data.description,        frequency=habit_data.frequency.name,        lastDoneAt=habit_data.lastDoneAt,        name=habit_data.name,        habitUser_id=habit_data.habitUser        )

    database.add(db_habit)
    database.flush()
    database.refresh(db_habit)

    if habit_data.progressEntries:
        # Validate that all ProgressEntry IDs exist
        for related_progressentry_id in habit_data.progressEntries:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail=f"ProgressEntry with id {related_progressentry_id} not found")

        # Update the related entities with the new foreign key
        database.query(ProgressEntry).filter(ProgressEntry.id.in_(habit_data.progressEntries)).update(
            {ProgressEntry.habit_id: db_habit.id}, synchronize_session=False
        )
        database.flush()




    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.habit_id == db_habit.id).all()
    response_data = {
        "habit": db_habit,
        "progressEntries_ids": [x[0] for x in progressEntries_ids]    }
    database.commit()
    database.refresh(db_habit)
    return response_data


@router.post("/habit/bulk/", response_model=None, tags=["Habit"])
async def bulk_create_habit(items: list[HabitCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Habit entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['progressEntries']):
        raise HTTPException(status_code=422, detail="Bulk creation of Habit with relationships is not supported; use POST /habit/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.habitUser:
                raise ValueError("User ID is required")

            db_habit = Habit(
                active=item_data.active,                currentStreak=item_data.currentStreak,                description=item_data.description,                frequency=item_data.frequency.name,                lastDoneAt=item_data.lastDoneAt,                name=item_data.name,                habitUser_id=item_data.habitUser            )
            database.add(db_habit)
            database.flush()  # Get ID without committing
            created_items.append(db_habit.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of Habit failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Habit entities"
    }


@router.delete("/habit/bulk/", response_model=None, tags=["Habit"])
async def bulk_delete_habit(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Habit entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_habit = database.query(Habit).filter(Habit.id == item_id).first()
        if db_habit:
            conflict = habit_delete_conflict(db_habit)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete Habit " + str(item_id) + ": " + conflict)
            database.delete(db_habit)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Habit entities"
    }

@router.put("/habit/{habit_id}/", response_model=None, tags=["Habit"])
async def update_habit(habit_id: int, habit_data: HabitCreate, database: Session = Depends(get_db)) -> Habit:
    db_habit = database.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    setattr(db_habit, 'active', habit_data.active)
    setattr(db_habit, 'currentStreak', habit_data.currentStreak)
    setattr(db_habit, 'description', habit_data.description)
    setattr(db_habit, 'frequency', habit_data.frequency.name)
    setattr(db_habit, 'lastDoneAt', habit_data.lastDoneAt)
    setattr(db_habit, 'name', habit_data.name)
    if habit_data.habitUser is not None:
        related_habitUser = database.query(User).filter(User.id == habit_data.habitUser).first()
        if not related_habitUser:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_habit, 'habitUser_id', habit_data.habitUser)
    if habit_data.progressEntries is not None:
        requested_progressEntries = set(habit_data.progressEntries)
        current_progressEntries = {
            getattr(item, 'id')
            for item in database.query(ProgressEntry).filter(ProgressEntry.habit_id == db_habit.id).all()
        }
        progressEntries_to_detach = current_progressEntries - requested_progressEntries
        if progressEntries_to_detach:
            database.query(ProgressEntry).filter(ProgressEntry.id.in_(progressEntries_to_detach)).update(
                {ProgressEntry.habit_id: None}, synchronize_session=False
            )
        progressEntries_to_attach = requested_progressEntries - current_progressEntries
        for related_progressentry_id in progressEntries_to_attach:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail="ProgressEntry with id " + str(related_progressentry_id) + " not found")
        if progressEntries_to_attach:
            database.query(ProgressEntry).filter(ProgressEntry.id.in_(progressEntries_to_attach)).update(
                {ProgressEntry.habit_id: db_habit.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_habit)

    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.habit_id == db_habit.id).all()
    response_data = {
        "habit": db_habit,
        "progressEntries_ids": [x[0] for x in progressEntries_ids]    }
    return response_data


def habit_delete_conflict(db_habit, deleting=None, wholes=()):
    """Why this Habit cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_habit)
        deleting = [db_habit] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    return None


@router.delete("/habit/{habit_id}/", response_model=None, tags=["Habit"])
async def delete_habit(habit_id: int, database: Session = Depends(get_db)):
    db_habit = database.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    conflict = habit_delete_conflict(db_habit)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete Habit " + str(habit_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_habit = {
        attr.key: getattr(db_habit, attr.key)
        for attr in db_habit.__mapper__.column_attrs
    }
    database.delete(db_habit)
    database.commit()
    return deleted_habit


@router.get("/habit/{habit_id}/progressEntries/", response_model=None, tags=["Habit Relationships"])
async def get_progressEntries_of_habit(habit_id: int, database: Session = Depends(get_db)):
    """Get all ProgressEntry entities related to this Habit through progressEntries"""
    db_habit = database.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    progressEntries_list = database.query(ProgressEntry).filter(ProgressEntry.habit_id == habit_id).all()

    return {
        "habit_id": habit_id,
        "progressEntries_count": len(progressEntries_list),
        "progressEntries": progressEntries_list
    }


