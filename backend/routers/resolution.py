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


@router.get("/resolution/", response_model=None, tags=["Resolution"])
def get_all_resolution(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Resolution)
        query = query.options(joinedload(Resolution.category))
        query = query.options(joinedload(Resolution.owner))
        resolution_list = query.all()

        # Serialize with relationships included
        result = []
        for db_resolution in resolution_list:
            item_dict = db_resolution.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if db_resolution.category:
                related_obj = db_resolution.category
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['category'] = related_dict
            else:
                item_dict['category'] = None
            if db_resolution.owner:
                related_obj = db_resolution.owner
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['owner'] = related_dict
            else:
                item_dict['owner'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            related_subgoal_list = database.query(SubGoal).filter(SubGoal.parentResolution_id == db_resolution.id).all()
            item_dict['subGoals'] = []
            for related_subgoal_obj in related_subgoal_list:
                related_subgoal_dict = related_subgoal_obj.__dict__.copy()
                related_subgoal_dict.pop('_sa_instance_state', None)
                item_dict['subGoals'].append(related_subgoal_dict)
            related_progressentry_list = database.query(ProgressEntry).filter(ProgressEntry.resolution_id == db_resolution.id).all()
            item_dict['progressEntries'] = []
            for related_progressentry_obj in related_progressentry_list:
                related_progressentry_dict = related_progressentry_obj.__dict__.copy()
                related_progressentry_dict.pop('_sa_instance_state', None)
                item_dict['progressEntries'].append(related_progressentry_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Resolution).all()


@router.get("/resolution/count/", response_model=None, tags=["Resolution"])
def get_count_resolution(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Resolution entities"""
    count = database.query(Resolution).count()
    return {"count": count}


@router.get("/resolution/paginated/", response_model=None, tags=["Resolution"])
def get_paginated_resolution(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Resolution entities"""
    total = database.query(Resolution).count()
    resolution_list = database.query(Resolution).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": resolution_list
        }

    result = []
    for db_resolution in resolution_list:
        subGoals_ids = database.query(SubGoal.id).filter(SubGoal.parentResolution_id == db_resolution.id).all()
        progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.resolution_id == db_resolution.id).all()
        item_data = {
            "resolution": db_resolution,
            "subGoals_ids": [x[0] for x in subGoals_ids],            "progressEntries_ids": [x[0] for x in progressEntries_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/resolution/search/", response_model=None, tags=["Resolution"])
def search_resolution(
    description: str = None,
    title: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Resolution entities by attributes"""
    query = database.query(Resolution)

    if description is not None:
        query = query.filter(Resolution.description.ilike(f"%{description}%"))
    if title is not None:
        query = query.filter(Resolution.title.ilike(f"%{title}%"))

    results = query.all()
    return results


@router.get("/resolution/{resolution_id}/", response_model=None, tags=["Resolution"])
async def get_resolution(resolution_id: int, database: Session = Depends(get_db)) -> Resolution:
    db_resolution = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if db_resolution is None:
        raise HTTPException(status_code=404, detail="Resolution not found")

    subGoals_ids = database.query(SubGoal.id).filter(SubGoal.parentResolution_id == db_resolution.id).all()
    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.resolution_id == db_resolution.id).all()
    response_data = {
        "resolution": db_resolution,
        "subGoals_ids": [x[0] for x in subGoals_ids],        "progressEntries_ids": [x[0] for x in progressEntries_ids]}
    return response_data



@router.post("/resolution/", response_model=None, tags=["Resolution"])
async def create_resolution(resolution_data: ResolutionCreate, database: Session = Depends(get_db)) -> Resolution:

    if resolution_data.category :
        related_category = database.query(Category).filter(Category.id == resolution_data.category).first()
        if not related_category:
            raise HTTPException(status_code=400, detail="Category not found")
    if resolution_data.owner is not None:
        related_owner = database.query(User).filter(User.id == resolution_data.owner).first()
        if not related_owner:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_resolution = Resolution(
        description=resolution_data.description,        status=resolution_data.status.name,        targetDate=resolution_data.targetDate,        title=resolution_data.title,        category_id=resolution_data.category,        owner_id=resolution_data.owner        )

    database.add(db_resolution)
    database.flush()
    database.refresh(db_resolution)

    if resolution_data.subGoals:
        # Validate that all SubGoal IDs exist
        for related_subgoal_id in resolution_data.subGoals:
            related_subgoal = database.query(SubGoal).filter(SubGoal.id == related_subgoal_id).first()
            if not related_subgoal:
                raise HTTPException(status_code=400, detail=f"SubGoal with id {related_subgoal_id} not found")

        # Update the related entities with the new foreign key
        database.query(SubGoal).filter(SubGoal.id.in_(resolution_data.subGoals)).update(
            {SubGoal.parentResolution_id: db_resolution.id}, synchronize_session=False
        )
        database.flush()
    if resolution_data.progressEntries:
        # Validate that all ProgressEntry IDs exist
        for related_progressentry_id in resolution_data.progressEntries:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail=f"ProgressEntry with id {related_progressentry_id} not found")

        # Update the related entities with the new foreign key
        database.query(ProgressEntry).filter(ProgressEntry.id.in_(resolution_data.progressEntries)).update(
            {ProgressEntry.resolution_id: db_resolution.id}, synchronize_session=False
        )
        database.flush()




    subGoals_ids = database.query(SubGoal.id).filter(SubGoal.parentResolution_id == db_resolution.id).all()
    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.resolution_id == db_resolution.id).all()
    response_data = {
        "resolution": db_resolution,
        "subGoals_ids": [x[0] for x in subGoals_ids],        "progressEntries_ids": [x[0] for x in progressEntries_ids]    }
    database.commit()
    database.refresh(db_resolution)
    return response_data


@router.post("/resolution/bulk/", response_model=None, tags=["Resolution"])
async def bulk_create_resolution(items: list[ResolutionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Resolution entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['subGoals', 'progressEntries']):
        raise HTTPException(status_code=422, detail="Bulk creation of Resolution with relationships is not supported; use POST /resolution/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.owner:
                raise ValueError("User ID is required")

            db_resolution = Resolution(
                description=item_data.description,                status=item_data.status.name,                targetDate=item_data.targetDate,                title=item_data.title,                category_id=item_data.category,                owner_id=item_data.owner            )
            database.add(db_resolution)
            database.flush()  # Get ID without committing
            created_items.append(db_resolution.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of Resolution failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Resolution entities"
    }


@router.delete("/resolution/bulk/", response_model=None, tags=["Resolution"])
async def bulk_delete_resolution(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Resolution entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_resolution = database.query(Resolution).filter(Resolution.id == item_id).first()
        if db_resolution:
            conflict = resolution_delete_conflict(db_resolution)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete Resolution " + str(item_id) + ": " + conflict)
            database.delete(db_resolution)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Resolution entities"
    }

@router.put("/resolution/{resolution_id}/", response_model=None, tags=["Resolution"])
async def update_resolution(resolution_id: int, resolution_data: ResolutionCreate, database: Session = Depends(get_db)) -> Resolution:
    db_resolution = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if db_resolution is None:
        raise HTTPException(status_code=404, detail="Resolution not found")

    setattr(db_resolution, 'description', resolution_data.description)
    setattr(db_resolution, 'status', resolution_data.status.name)
    setattr(db_resolution, 'targetDate', resolution_data.targetDate)
    setattr(db_resolution, 'title', resolution_data.title)
    if resolution_data.category is not None:
        related_category = database.query(Category).filter(Category.id == resolution_data.category).first()
        if not related_category:
            raise HTTPException(status_code=400, detail="Category not found")
        setattr(db_resolution, 'category_id', resolution_data.category)
    else:
        setattr(db_resolution, 'category_id', None)
    if resolution_data.owner is not None:
        related_owner = database.query(User).filter(User.id == resolution_data.owner).first()
        if not related_owner:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_resolution, 'owner_id', resolution_data.owner)
    if resolution_data.subGoals is not None:
        requested_subGoals = set(resolution_data.subGoals)
        current_subGoals = {
            getattr(item, 'id')
            for item in database.query(SubGoal).filter(SubGoal.parentResolution_id == db_resolution.id).all()
        }
        subGoals_to_detach = current_subGoals - requested_subGoals
        if subGoals_to_detach:
            raise HTTPException(status_code=409, detail="SubGoal " + ", ".join(str(item) for item in sorted(subGoals_to_detach)) + " requires a parentResolution: reassign it instead of removing it")
        subGoals_to_attach = requested_subGoals - current_subGoals
        for related_subgoal_id in subGoals_to_attach:
            related_subgoal = database.query(SubGoal).filter(SubGoal.id == related_subgoal_id).first()
            if not related_subgoal:
                raise HTTPException(status_code=400, detail="SubGoal with id " + str(related_subgoal_id) + " not found")
        if subGoals_to_attach:
            database.query(SubGoal).filter(SubGoal.id.in_(subGoals_to_attach)).update(
                {SubGoal.parentResolution_id: db_resolution.id}, synchronize_session=False
            )
    if resolution_data.progressEntries is not None:
        requested_progressEntries = set(resolution_data.progressEntries)
        current_progressEntries = {
            getattr(item, 'id')
            for item in database.query(ProgressEntry).filter(ProgressEntry.resolution_id == db_resolution.id).all()
        }
        progressEntries_to_detach = current_progressEntries - requested_progressEntries
        if progressEntries_to_detach:
            database.query(ProgressEntry).filter(ProgressEntry.id.in_(progressEntries_to_detach)).update(
                {ProgressEntry.resolution_id: None}, synchronize_session=False
            )
        progressEntries_to_attach = requested_progressEntries - current_progressEntries
        for related_progressentry_id in progressEntries_to_attach:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail="ProgressEntry with id " + str(related_progressentry_id) + " not found")
        if progressEntries_to_attach:
            database.query(ProgressEntry).filter(ProgressEntry.id.in_(progressEntries_to_attach)).update(
                {ProgressEntry.resolution_id: db_resolution.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_resolution)

    subGoals_ids = database.query(SubGoal.id).filter(SubGoal.parentResolution_id == db_resolution.id).all()
    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.resolution_id == db_resolution.id).all()
    response_data = {
        "resolution": db_resolution,
        "subGoals_ids": [x[0] for x in subGoals_ids],        "progressEntries_ids": [x[0] for x in progressEntries_ids]    }
    return response_data


def resolution_delete_conflict(db_resolution, deleting=None, wholes=()):
    """Why this Resolution cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_resolution)
        deleting = [db_resolution] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    if any(whole is db_resolution for whole in wholes):
        return "Resolution " + str(getattr(db_resolution, 'id')) + " is one of its own parts"
    from routers.subgoal import subgoal_delete_conflict
    parts_subGoals = db_resolution.subGoals
    for part in (list(parts_subGoals) if isinstance(parts_subGoals, list) else [item for item in [parts_subGoals] if item is not None]):
        conflict = subgoal_delete_conflict(part, deleting, wholes + (db_resolution,))
        if conflict:
            return "SubGoal " + str(getattr(part, 'id')) + " would be deleted with it, and " + conflict
    return None


@router.delete("/resolution/{resolution_id}/", response_model=None, tags=["Resolution"])
async def delete_resolution(resolution_id: int, database: Session = Depends(get_db)):
    db_resolution = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if db_resolution is None:
        raise HTTPException(status_code=404, detail="Resolution not found")
    conflict = resolution_delete_conflict(db_resolution)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete Resolution " + str(resolution_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_resolution = {
        attr.key: getattr(db_resolution, attr.key)
        for attr in db_resolution.__mapper__.column_attrs
    }
    database.delete(db_resolution)
    database.commit()
    return deleted_resolution


@router.get("/resolution/{resolution_id}/subGoals/", response_model=None, tags=["Resolution Relationships"])
async def get_subGoals_of_resolution(resolution_id: int, database: Session = Depends(get_db)):
    """Get all SubGoal entities related to this Resolution through subGoals"""
    db_resolution = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if db_resolution is None:
        raise HTTPException(status_code=404, detail="Resolution not found")

    subGoals_list = database.query(SubGoal).filter(SubGoal.parentResolution_id == resolution_id).all()

    return {
        "resolution_id": resolution_id,
        "subGoals_count": len(subGoals_list),
        "subGoals": subGoals_list
    }

@router.get("/resolution/{resolution_id}/progressEntries/", response_model=None, tags=["Resolution Relationships"])
async def get_progressEntries_of_resolution(resolution_id: int, database: Session = Depends(get_db)):
    """Get all ProgressEntry entities related to this Resolution through progressEntries"""
    db_resolution = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if db_resolution is None:
        raise HTTPException(status_code=404, detail="Resolution not found")

    progressEntries_list = database.query(ProgressEntry).filter(ProgressEntry.resolution_id == resolution_id).all()

    return {
        "resolution_id": resolution_id,
        "progressEntries_count": len(progressEntries_list),
        "progressEntries": progressEntries_list
    }


