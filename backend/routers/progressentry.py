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


@router.get("/progressentry/", response_model=None, tags=["ProgressEntry"])
def get_all_progressentry(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ProgressEntry)
        query = query.options(joinedload(ProgressEntry.author))
        query = query.options(joinedload(ProgressEntry.habit))
        query = query.options(joinedload(ProgressEntry.resolution))
        progressentry_list = query.all()

        # Serialize with relationships included
        result = []
        for db_progressentry in progressentry_list:
            item_dict = db_progressentry.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if db_progressentry.author:
                related_obj = db_progressentry.author
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['author'] = related_dict
            else:
                item_dict['author'] = None
            if db_progressentry.habit:
                related_obj = db_progressentry.habit
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['habit'] = related_dict
            else:
                item_dict['habit'] = None
            if db_progressentry.resolution:
                related_obj = db_progressentry.resolution
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['resolution'] = related_dict
            else:
                item_dict['resolution'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ProgressEntry).all()


@router.get("/progressentry/count/", response_model=None, tags=["ProgressEntry"])
def get_count_progressentry(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ProgressEntry entities"""
    count = database.query(ProgressEntry).count()
    return {"count": count}


@router.get("/progressentry/paginated/", response_model=None, tags=["ProgressEntry"])
def get_paginated_progressentry(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ProgressEntry entities"""
    total = database.query(ProgressEntry).count()
    progressentry_list = database.query(ProgressEntry).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": progressentry_list
    }
@router.get("/progressentry/search/", response_model=None, tags=["ProgressEntry"])
def search_progressentry(
    amount: float = None,
    notes: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search ProgressEntry entities by attributes"""
    query = database.query(ProgressEntry)

    if amount is not None:
        query = query.filter(ProgressEntry.amount == amount)
    if notes is not None:
        query = query.filter(ProgressEntry.notes.ilike(f"%{notes}%"))

    results = query.all()
    return results


@router.get("/progressentry/{progressentry_id}/", response_model=None, tags=["ProgressEntry"])
async def get_progressentry(progressentry_id: int, database: Session = Depends(get_db)) -> ProgressEntry:
    db_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == progressentry_id).first()
    if db_progressentry is None:
        raise HTTPException(status_code=404, detail="ProgressEntry not found")

    response_data = {
        "progressentry": db_progressentry,
}
    return response_data



@router.post("/progressentry/", response_model=None, tags=["ProgressEntry"])
async def create_progressentry(progressentry_data: ProgressEntryCreate, database: Session = Depends(get_db)) -> ProgressEntry:

    if progressentry_data.author is not None:
        related_author = database.query(User).filter(User.id == progressentry_data.author).first()
        if not related_author:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if progressentry_data.habit :
        related_habit = database.query(Habit).filter(Habit.id == progressentry_data.habit).first()
        if not related_habit:
            raise HTTPException(status_code=400, detail="Habit not found")
    if progressentry_data.resolution :
        related_resolution = database.query(Resolution).filter(Resolution.id == progressentry_data.resolution).first()
        if not related_resolution:
            raise HTTPException(status_code=400, detail="Resolution not found")

    db_progressentry = ProgressEntry(
        amount=progressentry_data.amount,        date=progressentry_data.date,        notes=progressentry_data.notes,        author_id=progressentry_data.author,        habit_id=progressentry_data.habit,        resolution_id=progressentry_data.resolution        )

    database.add(db_progressentry)
    database.flush()
    database.refresh(db_progressentry)





    database.commit()
    database.refresh(db_progressentry)
    return db_progressentry


@router.post("/progressentry/bulk/", response_model=None, tags=["ProgressEntry"])
async def bulk_create_progressentry(items: list[ProgressEntryCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ProgressEntry entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.author:
                raise ValueError("User ID is required")

            db_progressentry = ProgressEntry(
                amount=item_data.amount,                date=item_data.date,                notes=item_data.notes,                author_id=item_data.author,                habit_id=item_data.habit,                resolution_id=item_data.resolution            )
            database.add(db_progressentry)
            database.flush()  # Get ID without committing
            created_items.append(db_progressentry.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of ProgressEntry failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ProgressEntry entities"
    }


@router.delete("/progressentry/bulk/", response_model=None, tags=["ProgressEntry"])
async def bulk_delete_progressentry(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ProgressEntry entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == item_id).first()
        if db_progressentry:
            conflict = progressentry_delete_conflict(db_progressentry)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete ProgressEntry " + str(item_id) + ": " + conflict)
            database.delete(db_progressentry)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ProgressEntry entities"
    }

@router.put("/progressentry/{progressentry_id}/", response_model=None, tags=["ProgressEntry"])
async def update_progressentry(progressentry_id: int, progressentry_data: ProgressEntryCreate, database: Session = Depends(get_db)) -> ProgressEntry:
    db_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == progressentry_id).first()
    if db_progressentry is None:
        raise HTTPException(status_code=404, detail="ProgressEntry not found")

    setattr(db_progressentry, 'amount', progressentry_data.amount)
    setattr(db_progressentry, 'date', progressentry_data.date)
    setattr(db_progressentry, 'notes', progressentry_data.notes)
    if progressentry_data.author is not None:
        related_author = database.query(User).filter(User.id == progressentry_data.author).first()
        if not related_author:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_progressentry, 'author_id', progressentry_data.author)
    if progressentry_data.habit is not None:
        related_habit = database.query(Habit).filter(Habit.id == progressentry_data.habit).first()
        if not related_habit:
            raise HTTPException(status_code=400, detail="Habit not found")
        setattr(db_progressentry, 'habit_id', progressentry_data.habit)
    else:
        setattr(db_progressentry, 'habit_id', None)
    if progressentry_data.resolution is not None:
        related_resolution = database.query(Resolution).filter(Resolution.id == progressentry_data.resolution).first()
        if not related_resolution:
            raise HTTPException(status_code=400, detail="Resolution not found")
        setattr(db_progressentry, 'resolution_id', progressentry_data.resolution)
    else:
        setattr(db_progressentry, 'resolution_id', None)
    database.commit()
    database.refresh(db_progressentry)

    return db_progressentry


def progressentry_delete_conflict(db_progressentry, deleting=None, wholes=()):
    """Why this ProgressEntry cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_progressentry)
        deleting = [db_progressentry] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    return None


@router.delete("/progressentry/{progressentry_id}/", response_model=None, tags=["ProgressEntry"])
async def delete_progressentry(progressentry_id: int, database: Session = Depends(get_db)):
    db_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == progressentry_id).first()
    if db_progressentry is None:
        raise HTTPException(status_code=404, detail="ProgressEntry not found")
    conflict = progressentry_delete_conflict(db_progressentry)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete ProgressEntry " + str(progressentry_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_progressentry = {
        attr.key: getattr(db_progressentry, attr.key)
        for attr in db_progressentry.__mapper__.column_attrs
    }
    database.delete(db_progressentry)
    database.commit()
    return deleted_progressentry



