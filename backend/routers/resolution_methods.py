from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   Resolution Method Endpoints
############################################





@router.post("/resolution/{resolution_id}/methods/activate/", response_model=None, tags=["Resolution Methods"])
async def execute_resolution_activate(
    resolution_id: int,  # the Resolution that activate runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the activate method on a Resolution instance.

    Resolution.activate() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # Resolution.activate: load the instance
    _resolution_object = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if _resolution_object is None:
        raise HTTPException(status_code=404, detail="Resolution not found")
    # Resolution.activate
    raise HTTPException(
        status_code=501,
        detail="Method 'activate' of Resolution is modeled but has no implementation - 501, never a fake success",
    )






@router.post("/resolution/{resolution_id}/methods/complete/", response_model=None, tags=["Resolution Methods"])
async def execute_resolution_complete(
    resolution_id: int,  # the Resolution that complete runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the complete method on a Resolution instance.

    Resolution.complete() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # Resolution.complete: load the instance
    _resolution_object = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if _resolution_object is None:
        raise HTTPException(status_code=404, detail="Resolution not found")
    # Resolution.complete
    raise HTTPException(
        status_code=501,
        detail="Method 'complete' of Resolution is modeled but has no implementation - 501, never a fake success",
    )






@router.post("/resolution/{resolution_id}/methods/pause/", response_model=None, tags=["Resolution Methods"])
async def execute_resolution_pause(
    resolution_id: int,  # the Resolution that pause runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the pause method on a Resolution instance.

    Resolution.pause() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # Resolution.pause: load the instance
    _resolution_object = database.query(Resolution).filter(Resolution.id == resolution_id).first()
    if _resolution_object is None:
        raise HTTPException(status_code=404, detail="Resolution not found")
    # Resolution.pause
    raise HTTPException(
        status_code=501,
        detail="Method 'pause' of Resolution is modeled but has no implementation - 501, never a fake success",
    )

