# File: Backend/app/routes/budgets.py
# Description: API routes for budgets, now protected by authentication.

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Budget, status_code=201)
def create_budget_for_current_user(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Set a new monthly budget for the currently logged-in user.
    """
    return crud.create_budget(db=db, budget=budget, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Budget])
def read_budgets_for_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all budgets for the currently logged-in user.
    """
    return crud.get_budgets_by_user(db, user_id=current_user.id)

@router.get("/status/{category}/{period}", response_model=schemas.BudgetStatus)
def get_budget_status_for_current_user(
    category: str,
    period: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get the spending status for a specific budget for the currently logged-in user.
    """
    budget = crud.get_budget_by_category_and_period(db, user_id=current_user.id, category=category, period=period)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found for this category and period.")

    spent = crud.get_spending_for_period(db, user_id=current_user.id, category=category, period=period)
    remaining = budget.limit - spent

    return schemas.BudgetStatus(
        **budget.__dict__,
        spent=round(spent, 2),
        remaining=round(remaining, 2)
    )
