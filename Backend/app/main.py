# File: Backend/app/main.py
# Description: The main entry point for the FastAPI application.

from fastapi import FastAPI
from .routes import users, transactions, budgets, auth
from .database import engine
from . import models

# This line creates the database tables based on your SQLAlchemy models.
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="SmartPay API",
    description="Backend for SmartPay - Payment + Spending Analysis App",
    version="1.0.0"
)

# --- Best Practice Tip ---
# Add a simple root endpoint to confirm the API is running.
@app.get("/", tags=["Root"])
def read_root():
    """A simple endpoint to check if the API is alive."""
    return {"message": "Welcome to SmartPay API! See /docs for endpoint details."}


# --- Include Routers ---
# The auth router is added for handling login and token generation.
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["Budgets"])

# --- How to Run ---
# 1. Install new dependencies for authentication:
#    pip install "passlib[bcrypt]" "python-jose[cryptography]"
# 2. Make sure you are in the 'Backend' directory in your terminal.
# 3. Run the following command:
#    uvicorn app.main:app --reload
