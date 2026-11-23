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


@router.get("/user/", response_model=None, tags=["User"])
def get_all_user(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(User)
        user_list = query.all()

        # Serialize with relationships included
        result = []
        for db_user in user_list:
            item_dict = db_user.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            related_progressentry_list = database.query(ProgressEntry).filter(ProgressEntry.author_id == db_user.id).all()
            item_dict['progressEntries'] = []
            for related_progressentry_obj in related_progressentry_list:
                related_progressentry_dict = related_progressentry_obj.__dict__.copy()
                related_progressentry_dict.pop('_sa_instance_state', None)
                item_dict['progressEntries'].append(related_progressentry_dict)
            related_habit_list = database.query(Habit).filter(Habit.habitUser_id == db_user.id).all()
            item_dict['habits'] = []
            for related_habit_obj in related_habit_list:
                related_habit_dict = related_habit_obj.__dict__.copy()
                related_habit_dict.pop('_sa_instance_state', None)
                item_dict['habits'].append(related_habit_dict)
            related_resolution_list = database.query(Resolution).filter(Resolution.owner_id == db_user.id).all()
            item_dict['resolutions'] = []
            for related_resolution_obj in related_resolution_list:
                related_resolution_dict = related_resolution_obj.__dict__.copy()
                related_resolution_dict.pop('_sa_instance_state', None)
                item_dict['resolutions'].append(related_resolution_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(User).all()


@router.get("/user/count/", response_model=None, tags=["User"])
def get_count_user(database: Session = Depends(get_db)) -> dict:
    """Get the total count of User entities"""
    count = database.query(User).count()
    return {"count": count}


@router.get("/user/paginated/", response_model=None, tags=["User"])
def get_paginated_user(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of User entities"""
    total = database.query(User).count()
    user_list = database.query(User).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": user_list
        }

    result = []
    for db_user in user_list:
        progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.author_id == db_user.id).all()
        habits_ids = database.query(Habit.id).filter(Habit.habitUser_id == db_user.id).all()
        resolutions_ids = database.query(Resolution.id).filter(Resolution.owner_id == db_user.id).all()
        item_data = {
            "user": db_user,
            "progressEntries_ids": [x[0] for x in progressEntries_ids],            "habits_ids": [x[0] for x in habits_ids],            "resolutions_ids": [x[0] for x in resolutions_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/user/search/", response_model=None, tags=["User"])
def search_user(
    email: str = None,
    fullName: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search User entities by attributes"""
    query = database.query(User)

    if email is not None:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if fullName is not None:
        query = query.filter(User.fullName.ilike(f"%{fullName}%"))

    results = query.all()
    return results


@router.get("/user/{user_id}/", response_model=None, tags=["User"])
async def get_user(user_id: int, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.author_id == db_user.id).all()
    habits_ids = database.query(Habit.id).filter(Habit.habitUser_id == db_user.id).all()
    resolutions_ids = database.query(Resolution.id).filter(Resolution.owner_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "progressEntries_ids": [x[0] for x in progressEntries_ids],        "habits_ids": [x[0] for x in habits_ids],        "resolutions_ids": [x[0] for x in resolutions_ids]}
    return response_data



@router.post("/user/", response_model=None, tags=["User"])
async def create_user(user_data: UserCreate, database: Session = Depends(get_db)) -> User:


    db_user = User(
        email=user_data.email,        fullName=user_data.fullName,        lastLoginAt=user_data.lastLoginAt        )

    database.add(db_user)
    database.flush()
    database.refresh(db_user)

    if user_data.progressEntries:
        # Validate that all ProgressEntry IDs exist
        for related_progressentry_id in user_data.progressEntries:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail=f"ProgressEntry with id {related_progressentry_id} not found")

        # Update the related entities with the new foreign key
        database.query(ProgressEntry).filter(ProgressEntry.id.in_(user_data.progressEntries)).update(
            {ProgressEntry.author_id: db_user.id}, synchronize_session=False
        )
        database.flush()
    if user_data.habits:
        # Validate that all Habit IDs exist
        for related_habit_id in user_data.habits:
            related_habit = database.query(Habit).filter(Habit.id == related_habit_id).first()
            if not related_habit:
                raise HTTPException(status_code=400, detail=f"Habit with id {related_habit_id} not found")

        # Update the related entities with the new foreign key
        database.query(Habit).filter(Habit.id.in_(user_data.habits)).update(
            {Habit.habitUser_id: db_user.id}, synchronize_session=False
        )
        database.flush()
    if user_data.resolutions:
        # Validate that all Resolution IDs exist
        for related_resolution_id in user_data.resolutions:
            related_resolution = database.query(Resolution).filter(Resolution.id == related_resolution_id).first()
            if not related_resolution:
                raise HTTPException(status_code=400, detail=f"Resolution with id {related_resolution_id} not found")

        # Update the related entities with the new foreign key
        database.query(Resolution).filter(Resolution.id.in_(user_data.resolutions)).update(
            {Resolution.owner_id: db_user.id}, synchronize_session=False
        )
        database.flush()




    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.author_id == db_user.id).all()
    habits_ids = database.query(Habit.id).filter(Habit.habitUser_id == db_user.id).all()
    resolutions_ids = database.query(Resolution.id).filter(Resolution.owner_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "progressEntries_ids": [x[0] for x in progressEntries_ids],        "habits_ids": [x[0] for x in habits_ids],        "resolutions_ids": [x[0] for x in resolutions_ids]    }
    database.commit()
    database.refresh(db_user)
    return response_data


@router.post("/user/bulk/", response_model=None, tags=["User"])
async def bulk_create_user(items: list[UserCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple User entities at once"""
    if any(getattr(item, field, None) for item in items for field in ['progressEntries', 'habits', 'resolutions']):
        raise HTTPException(status_code=422, detail="Bulk creation of User with relationships is not supported; use POST /user/ to validate and persist its relationships")
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_user = User(
                email=item_data.email,                fullName=item_data.fullName,                lastLoginAt=item_data.lastLoginAt            )
            database.add(db_user)
            database.flush()  # Get ID without committing
            created_items.append(db_user.id)
        except ValueError as e:
            errors.append({"index": idx, "error": str(e)})
        except IntegrityError as e:
            # The driver's text goes to the log; a failed flush ends the session's work.
            logger.error("Bulk creation of User failed at item %s: %s", idx, e)
            errors.append({"index": idx, "error": integrity_error_detail(e)})
            break

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} User entities"
    }


@router.delete("/user/bulk/", response_model=None, tags=["User"])
async def bulk_delete_user(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple User entities at once"""
    # Aggregate deletion must account for every related lower bound. Until it
    # shares that validation, use the guarded individual delete endpoint.
    if ids:
        raise HTTPException(status_code=409, detail="Bulk deletion of User can violate required relationships and is not supported; use the individual DELETE /user/ endpoint")
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_user = database.query(User).filter(User.id == item_id).first()
        if db_user:
            conflict = user_delete_conflict(db_user)
            if conflict:
                raise HTTPException(status_code=409, detail="Cannot delete User " + str(item_id) + ": " + conflict)
            database.delete(db_user)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} User entities"
    }

@router.put("/user/{user_id}/", response_model=None, tags=["User"])
async def update_user(user_id: int, user_data: UserCreate, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(db_user, 'email', user_data.email)
    setattr(db_user, 'fullName', user_data.fullName)
    setattr(db_user, 'lastLoginAt', user_data.lastLoginAt)
    if user_data.progressEntries is not None:
        requested_progressEntries = set(user_data.progressEntries)
        current_progressEntries = {
            getattr(item, 'id')
            for item in database.query(ProgressEntry).filter(ProgressEntry.author_id == db_user.id).all()
        }
        progressEntries_to_detach = current_progressEntries - requested_progressEntries
        if progressEntries_to_detach:
            raise HTTPException(status_code=409, detail="ProgressEntry " + ", ".join(str(item) for item in sorted(progressEntries_to_detach)) + " requires a author: reassign it instead of removing it")
        progressEntries_to_attach = requested_progressEntries - current_progressEntries
        for related_progressentry_id in progressEntries_to_attach:
            related_progressentry = database.query(ProgressEntry).filter(ProgressEntry.id == related_progressentry_id).first()
            if not related_progressentry:
                raise HTTPException(status_code=400, detail="ProgressEntry with id " + str(related_progressentry_id) + " not found")
        if progressEntries_to_attach:
            database.query(ProgressEntry).filter(ProgressEntry.id.in_(progressEntries_to_attach)).update(
                {ProgressEntry.author_id: db_user.id}, synchronize_session=False
            )
    if user_data.habits is not None:
        requested_habits = set(user_data.habits)
        current_habits = {
            getattr(item, 'id')
            for item in database.query(Habit).filter(Habit.habitUser_id == db_user.id).all()
        }
        habits_to_detach = current_habits - requested_habits
        if habits_to_detach:
            raise HTTPException(status_code=409, detail="Habit " + ", ".join(str(item) for item in sorted(habits_to_detach)) + " requires a habitUser: reassign it instead of removing it")
        habits_to_attach = requested_habits - current_habits
        for related_habit_id in habits_to_attach:
            related_habit = database.query(Habit).filter(Habit.id == related_habit_id).first()
            if not related_habit:
                raise HTTPException(status_code=400, detail="Habit with id " + str(related_habit_id) + " not found")
        if habits_to_attach:
            database.query(Habit).filter(Habit.id.in_(habits_to_attach)).update(
                {Habit.habitUser_id: db_user.id}, synchronize_session=False
            )
    if user_data.resolutions is not None:
        requested_resolutions = set(user_data.resolutions)
        current_resolutions = {
            getattr(item, 'id')
            for item in database.query(Resolution).filter(Resolution.owner_id == db_user.id).all()
        }
        resolutions_to_detach = current_resolutions - requested_resolutions
        if resolutions_to_detach:
            raise HTTPException(status_code=409, detail="Resolution " + ", ".join(str(item) for item in sorted(resolutions_to_detach)) + " requires a owner: reassign it instead of removing it")
        resolutions_to_attach = requested_resolutions - current_resolutions
        for related_resolution_id in resolutions_to_attach:
            related_resolution = database.query(Resolution).filter(Resolution.id == related_resolution_id).first()
            if not related_resolution:
                raise HTTPException(status_code=400, detail="Resolution with id " + str(related_resolution_id) + " not found")
        if resolutions_to_attach:
            database.query(Resolution).filter(Resolution.id.in_(resolutions_to_attach)).update(
                {Resolution.owner_id: db_user.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_user)

    progressEntries_ids = database.query(ProgressEntry.id).filter(ProgressEntry.author_id == db_user.id).all()
    habits_ids = database.query(Habit.id).filter(Habit.habitUser_id == db_user.id).all()
    resolutions_ids = database.query(Resolution.id).filter(Resolution.owner_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "progressEntries_ids": [x[0] for x in progressEntries_ids],        "habits_ids": [x[0] for x in habits_ids],        "resolutions_ids": [x[0] for x in resolutions_ids]    }
    return response_data


def user_delete_conflict(db_user, deleting=None, wholes=()):
    """Why this User cannot be deleted (None when it can): a related record
    would be left without a link it requires. Covers the parts deleted with it;
    ``deleting`` holds every record of the delete, since none of them can block it,
    and ``wholes`` the records on the way down to this part."""
    if deleting is None:
        state = sa_inspect(db_user)
        deleting = [db_user] + [item[0] for item in state.mapper.cascade_iterator("delete", state)]
    related_progressEntries = db_user.progressEntries
    for related in (list(related_progressEntries) if isinstance(related_progressEntries, list) else [item for item in [related_progressEntries] if item is not None]):
        remaining = 0
        if related not in deleting and remaining < 1:
            return "ProgressEntry " + str(getattr(related, 'id')) + " requires at least 1 author"
    related_resolutions = db_user.resolutions
    for related in (list(related_resolutions) if isinstance(related_resolutions, list) else [item for item in [related_resolutions] if item is not None]):
        remaining = 0
        if related not in deleting and remaining < 1:
            return "Resolution " + str(getattr(related, 'id')) + " requires at least 1 owner"
    if any(whole is db_user for whole in wholes):
        return "User " + str(getattr(db_user, 'id')) + " is one of its own parts"
    from routers.habit import habit_delete_conflict
    parts_habits = db_user.habits
    for part in (list(parts_habits) if isinstance(parts_habits, list) else [item for item in [parts_habits] if item is not None]):
        conflict = habit_delete_conflict(part, deleting, wholes + (db_user,))
        if conflict:
            return "Habit " + str(getattr(part, 'id')) + " would be deleted with it, and " + conflict
    return None


@router.delete("/user/{user_id}/", response_model=None, tags=["User"])
async def delete_user(user_id: int, database: Session = Depends(get_db)):
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    conflict = user_delete_conflict(db_user)
    if conflict:
        raise HTTPException(status_code=409, detail="Cannot delete User " + str(user_id) + ": " + conflict)
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_user = {
        attr.key: getattr(db_user, attr.key)
        for attr in db_user.__mapper__.column_attrs
    }
    database.delete(db_user)
    database.commit()
    return deleted_user


@router.get("/user/{user_id}/progressEntries/", response_model=None, tags=["User Relationships"])
async def get_progressEntries_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all ProgressEntry entities related to this User through progressEntries"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    progressEntries_list = database.query(ProgressEntry).filter(ProgressEntry.author_id == user_id).all()

    return {
        "user_id": user_id,
        "progressEntries_count": len(progressEntries_list),
        "progressEntries": progressEntries_list
    }

@router.get("/user/{user_id}/habits/", response_model=None, tags=["User Relationships"])
async def get_habits_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Habit entities related to this User through habits"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    habits_list = database.query(Habit).filter(Habit.habitUser_id == user_id).all()

    return {
        "user_id": user_id,
        "habits_count": len(habits_list),
        "habits": habits_list
    }

@router.get("/user/{user_id}/resolutions/", response_model=None, tags=["User Relationships"])
async def get_resolutions_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Resolution entities related to this User through resolutions"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    resolutions_list = database.query(Resolution).filter(Resolution.owner_id == user_id).all()

    return {
        "user_id": user_id,
        "resolutions_count": len(resolutions_list),
        "resolutions": resolutions_list
    }


