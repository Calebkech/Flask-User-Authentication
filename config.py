from decouple import config
import os

# Try to get the DATABASE_URL from the environment variables
DATABASE_URI = config("DATABASE_URL", default=None)

# If DATABASE_URL is not found or it's a PostgreSQL URI but the database is not available, switch to SQLite
if DATABASE_URI is None or (DATABASE_URI.startswith("postgres://") and not os.getenv("POSTGRES_AVAILABLE", "false").lower() == "true"):
    DATABASE_URI = "sqlite:///app.db"  # Default to SQLite for testing

# Replace "postgres://" with "postgresql://" if necessary
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="guess-me")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False