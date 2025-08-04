# File: Backend/app/routes/transactions.py
# Description: API routes for transactions, now protected by authentication.

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Transaction, status_code=201)
def create_transaction_for_current_user(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Record a new transaction for the currently logged-in user.
    """
    return crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions_for_current_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all transactions for the currently logged-in user.
    """
    transactions = crud.get_transactions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

