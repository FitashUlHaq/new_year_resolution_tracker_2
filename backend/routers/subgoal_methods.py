from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   SubGoal Method Endpoints
############################################





@router.post("/subgoal/{subgoal_id}/methods/markComplete/", response_model=None, tags=["SubGoal Methods"])
async def execute_subgoal_markComplete(
    subgoal_id: int,  # the SubGoal that markComplete runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the markComplete method on a SubGoal instance.

    SubGoal.markComplete() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # SubGoal.markComplete: load the instance
    _subgoal_object = database.query(SubGoal).filter(SubGoal.id == subgoal_id).first()
    if _subgoal_object is None:
        raise HTTPException(status_code=404, detail="SubGoal not found")
    # SubGoal.markComplete
    raise HTTPException(
        status_code=501,
        detail="Method 'markComplete' of SubGoal is modeled but has no implementation - 501, never a fake success",
    )

