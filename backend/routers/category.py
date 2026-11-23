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


@router.get("/category/", response_model=None, tags=["Category"])
def get_all_category(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Category)
        category_list = query.all()

        # Serialize with relationships included
        result = []
        for db_category in category_list:
            item_dict = db_category.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            related_resolution_list = database.query(Resolution).filter(Resolution.category_id == db_category.id).all()
            item_dict['resolutions'] = []
            for related_resolution_obj in related_resolution_list:
                related_resolution_dict = related_resolution_obj.__dict__.copy()
                related_resolution_dict.pop('_sa_instance_state', None)
                item_dict['resolutions'].append(related_resolution_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Category).all()


@router.get("/category/count/", response_model=None, tags=["Category"])
def get_count_category(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Category entities"""
    count = database.query(Category).count()
    return {"count": count}


@router.get("/category/paginated/", response_model=None, tags=["Category"])
def get_paginated_category(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Category entities"""
    total = database.query(Category).count()
    category_list = database.query(Category).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": category_list
        }

    result = []
    for db_category in category_list:
        resolutions_ids = database.query(Resolution.id).filter(Resolution.category_id == db_category.id).all()
        item_data = {
            "category": db_category,
            "resolutions_ids": [x[0] for x in resolutions_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/category/search/", response_model=None, tags=["Category"])
def search_category(
    colorHex: str = None,
    name: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Category entities by attributes"""
    query = database.query(Category)

    if colorHex is not None:
        query = query.filter(Category.colorHex.ilike(f"%{colorHex}%"))
    if name is not None:
        query = query.filter(Category.name.ilike(f"%{name}%"))

    results = query.all()
    return results


@router.get("/category/{category_id}/", response_model=None, tags=["Category"])
async def get_category(category_id: int, database: Session = Depends(get_db)) -> Category:
    db_category = database.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    resolutions_ids = database.query(Resolution.id).filter(Resolution.category_id == db_category.id).all()
    response_data = {
        "category": db_category,
        "resolutions_ids": [x[0] for x in resolutions_ids]}
    return response_data



@router.post("/category/", response_model=None, tags=["Category"])
async def create_category(category_data: CategoryCreate, database: Session = Depends(get_db)) -> Category:


    db_category = Category(
        colorHex=category_data.colorHex,        name=category_data.name        )

    database.add(db_category)
    database.flush()
    database.refresh(db_category)

    if category_data.resolutions:
        # Validate that all Resolution IDs exist
        for related_resolution_id in category_data.resolutions:
            related_resolution = database.query(Resolution).filter(Resolution.id == related_resolution_id).first()
            if not related_resolution:
                raise HTTPException(status_code=400, detail=f"Resolution with id {related_resolution_id} not found")

        # Update the related entities with the new foreign key
        database.query(Resolution).filter(Resolution.id.in_(category_data.resolutions)).update(
            {Resolution.category_id: db_category.id}, synchronize_session=False
        )
        database.flush()




    resolutions_ids = database.query(Resolution.id).filter(Resolution.category_id == db_category.id).all()
    response_data = {
        "category": db_category,
        "resolutions_ids": [x[0] for x in resolutions_ids]    }
    database.commit()
    database.refresh(db_category)
    return response_data


@router.post("/category/bulk/", response_model=None, tags=["Category"])
async def bulk_create_category(items: list[CategoryCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Category entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['resolutions']):
        raise HTTPException(status_code=422, detail="Bulk creation of Category with relationships is not supported; use POST /category/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_category = Category(
                colorHex=item_data.colorHex,                name=item_data.name            )
            database.add(db_category)
            database.flush()  # Get ID without committing
            created_items.append(db_category.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of Category failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Category entities"
    }


@router.delete("/category/bulk/", response_model=None, tags=["Category"])
async def bulk_delete_category(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Category entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_category = database.query(Category).filter(Category.id == item_id).first()
        if db_category:
            conflict = category_delete_conflict(db_category)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete Category " + str(item_id) + ": " + conflict)
            database.delete(db_category)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Category entities"
    }

@router.put("/category/{category_id}/", response_model=None, tags=["Category"])
async def update_category(category_id: int, category_data: CategoryCreate, database: Session = Depends(get_db)) -> Category:
    db_category = database.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    setattr(db_category, 'colorHex', category_data.colorHex)
    setattr(db_category, 'name', category_data.name)
    if category_data.resolutions is not None:
        requested_resolutions = set(category_data.resolutions)
        current_resolutions = {
            getattr(item, 'id')
            for item in database.query(Resolution).filter(Resolution.category_id == db_category.id).all()
        }
        resolutions_to_detach = current_resolutions - requested_resolutions
        if resolutions_to_detach:
            database.query(Resolution).filter(Resolution.id.in_(resolutions_to_detach)).update(
                {Resolution.category_id: None}, synchronize_session=False
            )
        resolutions_to_attach = requested_resolutions - current_resolutions
        for related_resolution_id in resolutions_to_attach:
            related_resolution = database.query(Resolution).filter(Resolution.id == related_resolution_id).first()
            if not related_resolution:
                raise HTTPException(status_code=400, detail="Resolution with id " + str(related_resolution_id) + " not found")
        if resolutions_to_attach:
            database.query(Resolution).filter(Resolution.id.in_(resolutions_to_attach)).update(
                {Resolution.category_id: db_category.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_category)

    resolutions_ids = database.query(Resolution.id).filter(Resolution.category_id == db_category.id).all()
    response_data = {
        "category": db_category,
        "resolutions_ids": [x[0] for x in resolutions_ids]    }
    return response_data


def category_delete_conflict(db_category, deleting=None, wholes=()):
    """Why this Category cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_category)
        deleting = [db_category] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    return None


@router.delete("/category/{category_id}/", response_model=None, tags=["Category"])
async def delete_category(category_id: int, database: Session = Depends(get_db)):
    db_category = database.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    conflict = category_delete_conflict(db_category)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete Category " + str(category_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_category = {
        attr.key: getattr(db_category, attr.key)
        for attr in db_category.__mapper__.column_attrs
    }
    database.delete(db_category)
    database.commit()
    return deleted_category


@router.get("/category/{category_id}/resolutions/", response_model=None, tags=["Category Relationships"])
async def get_resolutions_of_category(category_id: int, database: Session = Depends(get_db)):
    """Get all Resolution entities related to this Category through resolutions"""
    db_category = database.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    resolutions_list = database.query(Resolution).filter(Resolution.category_id == category_id).all()

    return {
        "category_id": category_id,
        "resolutions_count": len(resolutions_list),
        "resolutions": resolutions_list
    }


