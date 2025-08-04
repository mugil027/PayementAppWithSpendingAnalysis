# File: Backend/app/crud.py
# Description: Contains all the CRUD (Create, Read, Update, Delete) database operations.

from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from . import models, schemas
from .auth import get_password_hash

# --- User CRUD ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Transaction CRUD ---

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

# --- Budget & Spending Analysis CRUD ---

def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    db_budget = models.Budget(**budget.model_dump(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets_by_user(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()

def get_budget_by_category_and_period(db: Session, user_id: int, category: str, period: str):
    return db.query(models.Budget).filter(
        models.Budget.user_id == user_id,
        models.Budget.category == category,
        models.Budget.period == period
    ).first()

def get_spending_for_period(db: Session, user_id: int, category: str, period: str):
    try:
        year, month = map(int, period.split('-'))
    except ValueError:
        return 0.0
    total_spent = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.category == category,
        extract('year', models.Transaction.timestamp) == year,
        extract('month', models.Transaction.timestamp) == month
    ).scalar()
    return total_spent or 0.0