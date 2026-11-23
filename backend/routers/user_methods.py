from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   User Method Endpoints
############################################





@router.post("/user/{user_id}/methods/addProgressEntry/", response_model=None, tags=["User Methods"])
async def execute_user_addProgressEntry(
    user_id: int,  # the User that addProgressEntry runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the addProgressEntry method on a User instance.

    Parameters:
    - resolution: Resolution    - entry: ProgressEntry    """
    # User.addProgressEntry: load the instance
    _user_object = database.query(User).filter(User.id == user_id).first()
    if _user_object is None:
        raise HTTPException(status_code=404, detail="User not found")
    # User.addProgressEntry
    raise HTTPException(
        status_code=501,
        detail="Method 'addProgressEntry' of User is modeled but has no implementation - 501, never a fake success",
    )






@router.post("/user/{user_id}/methods/createResolution/", response_model=None, tags=["User Methods"])
async def execute_user_createResolution(
    user_id: int,  # the User that createResolution runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the createResolution method on a User instance.

    Parameters:
    - title: str    - description: str    """
    # User.createResolution: load the instance
    _user_object = database.query(User).filter(User.id == user_id).first()
    if _user_object is None:
        raise HTTPException(status_code=404, detail="User not found")
    # User.createResolution
    raise HTTPException(
        status_code=501,
        detail="Method 'createResolution' of User is modeled but has no implementation - 501, never a fake success",
    )

