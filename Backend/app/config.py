# File: Backend/app/config.py
# Description: Manages application settings and environment variables.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Database Configuration ---
    # The default value points to the local SQLite DB.
    # For deployment, this will be overridden by the DATABASE_URL environment variable.
    DATABASE_URL: str = "sqlite:///./smartpay.db"

    # --- JWT Authentication Configuration ---
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # This tells Pydantic to load variables from a .env file
        env_file = ".env"

# Create a single instance of the settings to be used throughout the app
settings = Settings()
