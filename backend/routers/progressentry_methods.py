from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   ProgressEntry Method Endpoints
############################################





@router.post("/progressentry/{progressentry_id}/methods/edit/", response_model=None, tags=["ProgressEntry Methods"])
async def execute_progressentry_edit(
    progressentry_id: int,  # the ProgressEntry that edit runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the edit method on a ProgressEntry instance.

    Parameters:
    - notes: str    - amount: float    """
    # ProgressEntry.edit: load the instance
    _progressentry_object = database.query(ProgressEntry).filter(ProgressEntry.id == progressentry_id).first()
    if _progressentry_object is None:
        raise HTTPException(status_code=404, detail="ProgressEntry not found")
    # ProgressEntry.edit
    raise HTTPException(
        status_code=501,
        detail="Method 'edit' of ProgressEntry is modeled but has no implementation - 501, never a fake success",
    )






@router.post("/progressentry/{progressentry_id}/methods/remove/", response_model=None, tags=["ProgressEntry Methods"])
async def execute_progressentry_remove(
    progressentry_id: int,  # the ProgressEntry that remove runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the remove method on a ProgressEntry instance.

    ProgressEntry.remove() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # ProgressEntry.remove: load the instance
    _progressentry_object = database.query(ProgressEntry).filter(ProgressEntry.id == progressentry_id).first()
    if _progressentry_object is None:
        raise HTTPException(status_code=404, detail="ProgressEntry not found")
    # ProgressEntry.remove
    raise HTTPException(
        status_code=501,
        detail="Method 'remove' of ProgressEntry is modeled but has no implementation - 501, never a fake success",
    )

