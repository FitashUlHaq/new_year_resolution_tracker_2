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


@router.get("/subgoal/", response_model=None, tags=["SubGoal"])
def get_all_subgoal(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(SubGoal)
        query = query.options(joinedload(SubGoal.parentResolution))
        subgoal_list = query.all()

        # Serialize with relationships included
        result = []
        for db_subgoal in subgoal_list:
            item_dict = db_subgoal.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if db_subgoal.parentResolution:
                related_obj = db_subgoal.parentResolution
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['parentResolution'] = related_dict
            else:
                item_dict['parentResolution'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(SubGoal).all()


@router.get("/subgoal/count/", response_model=None, tags=["SubGoal"])
def get_count_subgoal(database: Session = Depends(get_db)) -> dict:
    """Get the total count of SubGoal entities"""
    count = database.query(SubGoal).count()
    return {"count": count}


@router.get("/subgoal/paginated/", response_model=None, tags=["SubGoal"])
def get_paginated_subgoal(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of SubGoal entities"""
    total = database.query(SubGoal).count()
    subgoal_list = database.query(SubGoal).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": subgoal_list
    }
@router.get("/subgoal/search/", response_model=None, tags=["SubGoal"])
def search_subgoal(
    completed: bool = None,
    description: str = None,
    title: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search SubGoal entities by attributes"""
    query = database.query(SubGoal)

    if completed is not None:
        query = query.filter(SubGoal.completed == completed)
    if description is not None:
        query = query.filter(SubGoal.description.ilike(f"%{description}%"))
    if title is not None:
        query = query.filter(SubGoal.title.ilike(f"%{title}%"))

    results = query.all()
    return results


@router.get("/subgoal/{subgoal_id}/", response_model=None, tags=["SubGoal"])
async def get_subgoal(subgoal_id: int, database: Session = Depends(get_db)) -> SubGoal:
    db_subgoal = database.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
    if db_subgoal is None:
        raise HTTPException(status_code=404, detail="SubGoal not found")

    response_data = {
        "subgoal": db_subgoal,
}
    return response_data



@router.post("/subgoal/", response_model=None, tags=["SubGoal"])
async def create_subgoal(subgoal_data: SubGoalCreate, database: Session = Depends(get_db)) -> SubGoal:

    if subgoal_data.parentResolution is not None:
        related_parentResolution = database.query(Resolution).filter(Resolution.id == subgoal_data.parentResolution).first()
        if not related_parentResolution:
            raise HTTPException(status_code=400, detail="Resolution not found")
    else:
        raise HTTPException(status_code=400, detail="Resolution ID is required")

    db_subgoal = SubGoal(
        completed=subgoal_data.completed,        description=subgoal_data.description,        targetDate=subgoal_data.targetDate,        title=subgoal_data.title,        parentResolution_id=subgoal_data.parentResolution        )

    database.add(db_subgoal)
    database.flush()
    database.refresh(db_subgoal)





    database.commit()
    database.refresh(db_subgoal)
    return db_subgoal


@router.post("/subgoal/bulk/", response_model=None, tags=["SubGoal"])
async def bulk_create_subgoal(items: list[SubGoalCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple SubGoal entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.parentResolution:
                raise ValueError("Resolution ID is required")

            db_subgoal = SubGoal(
                completed=item_data.completed,                description=item_data.description,                targetDate=item_data.targetDate,                title=item_data.title,                parentResolution_id=item_data.parentResolution            )
            database.add(db_subgoal)
            database.flush()  # Get ID without committing
            created_items.append(db_subgoal.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of SubGoal failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} SubGoal entities"
    }


@router.delete("/subgoal/bulk/", response_model=None, tags=["SubGoal"])
async def bulk_delete_subgoal(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple SubGoal entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_subgoal = database.query(SubGoal).filter(SubGoal.id == item_id).first()
        if db_subgoal:
            conflict = subgoal_delete_conflict(db_subgoal)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete SubGoal " + str(item_id) + ": " + conflict)
            database.delete(db_subgoal)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} SubGoal entities"
    }

@router.put("/subgoal/{subgoal_id}/", response_model=None, tags=["SubGoal"])
async def update_subgoal(subgoal_id: int, subgoal_data: SubGoalCreate, database: Session = Depends(get_db)) -> SubGoal:
    db_subgoal = database.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
    if db_subgoal is None:
        raise HTTPException(status_code=404, detail="SubGoal not found")

    setattr(db_subgoal, 'completed', subgoal_data.completed)
    setattr(db_subgoal, 'description', subgoal_data.description)
    setattr(db_subgoal, 'targetDate', subgoal_data.targetDate)
    setattr(db_subgoal, 'title', subgoal_data.title)
    if subgoal_data.parentResolution is not None:
        related_parentResolution = database.query(Resolution).filter(Resolution.id == subgoal_data.parentResolution).first()
        if not related_parentResolution:
            raise HTTPException(status_code=400, detail="Resolution not found")
        setattr(db_subgoal, 'parentResolution_id', subgoal_data.parentResolution)
    database.commit()
    database.refresh(db_subgoal)

    return db_subgoal


def subgoal_delete_conflict(db_subgoal, deleting=None, wholes=()):
    """Why this SubGoal cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_subgoal)
        deleting = [db_subgoal] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    return None


@router.delete("/subgoal/{subgoal_id}/", response_model=None, tags=["SubGoal"])
async def delete_subgoal(subgoal_id: int, database: Session = Depends(get_db)):
    db_subgoal = database.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
    if db_subgoal is None:
        raise HTTPException(status_code=404, detail="SubGoal not found")
    conflict = subgoal_delete_conflict(db_subgoal)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete SubGoal " + str(subgoal_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_subgoal = {
        attr.key: getattr(db_subgoal, attr.key)
        for attr in db_subgoal.__mapper__.column_attrs
    }
    database.delete(db_subgoal)
    database.commit()
    return deleted_subgoal



