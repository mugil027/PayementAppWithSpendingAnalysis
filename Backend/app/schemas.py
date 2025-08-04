# File: Backend/app/schemas.py
# Description: Pydantic models (schemas) for API validation and response models.

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    amount: float = Field(gt=0, description="The transaction amount must be positive")
    category: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True

# --- Budget Schemas ---
class BudgetBase(BaseModel):
    category: str
    limit: float = Field(gt=0, description="The budget limit must be positive")
    period: str # e.g., "2025-08"

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BudgetStatus(Budget):
    spent: float
    remaining: float

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    transactions: List[Transaction] = []
    budgets: List[Budget] = []

    class Config:
        from_attributes = True
