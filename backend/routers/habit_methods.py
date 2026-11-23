from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()

############################################
#   Habit Method Endpoints
############################################





@router.post("/habit/{habit_id}/methods/markDone/", response_model=None, tags=["Habit Methods"])
async def execute_habit_markDone(
    habit_id: int,  # the Habit that markDone runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the markDone method on a Habit instance.

    Parameters:
    - doneAt: datetime    """
    # Habit.markDone: load the instance
    _habit_object = database.query(Habit).filter(Habit.id == habit_id).first()
    if _habit_object is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    # Habit.markDone
    raise HTTPException(
        status_code=501,
        detail="Method 'markDone' of Habit is modeled but has no implementation - 501, never a fake success",
    )






@router.post("/habit/{habit_id}/methods/resetStreak/", response_model=None, tags=["Habit Methods"])
async def execute_habit_resetStreak(
    habit_id: int,  # the Habit that resetStreak runs on
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """Execute the resetStreak method on a Habit instance.

    Habit.resetStreak() is declared with no parameters, and the button sends none.
    An empty request body must succeed - default any value the spec leaves open, never demand it.
    """
    # Habit.resetStreak: load the instance
    _habit_object = database.query(Habit).filter(Habit.id == habit_id).first()
    if _habit_object is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    # Habit.resetStreak
    raise HTTPException(
        status_code=501,
        detail="Method 'resetStreak' of Habit is modeled but has no implementation - 501, never a fake success",
    )

