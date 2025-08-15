"""
Simple database migration system.
For production use, consider using Alembic.
"""
import logging
from sqlalchemy import text
from app.core.database import engine, Base
from app.models import user, blog

logger = logging.getLogger(__name__)


def run_migrations():
    """Run database migrations."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Run any additional migrations
        with engine.connect() as connection:
            # Add indexes if they don't exist
            create_indexes(connection)
            
            # Add any data migrations
            run_data_migrations(connection)
            
        logger.info("Database migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


def create_indexes(connection):
    """Create additional database indexes."""
    try:
        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)",
            "CREATE INDEX IF NOT EXISTS idx_blogs_title ON blogs(title)",
            "CREATE INDEX IF NOT EXISTS idx_blogs_creator_id ON blogs(creator_id)",
            "CREATE INDEX IF NOT EXISTS idx_blogs_created_at ON blogs(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_blogs_published ON blogs(is_published)",
        ]
        
        for index_sql in indexes:
            connection.execute(text(index_sql))
        
        connection.commit()
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Index creation failed (may already exist): {e}")


def run_data_migrations(connection):
    """Run data migrations."""
    try:
        # Check if we need to run any data migrations
        # This is where you would add logic for data transformations
        
        # Example: Update existing records if needed
        # connection.execute(text("UPDATE users SET is_verified = true WHERE is_verified IS NULL"))
        
        connection.commit()
        logger.info("Data migrations completed successfully")
        
    except Exception as e:
        logger.warning(f"Data migration failed: {e}")


def check_migration_status():
    """Check the current migration status."""
    try:
        with engine.connect() as connection:
            # Check if tables exist
            result = connection.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('users', 'blogs')
            """))
            
            existing_tables = [row[0] for row in result]
            
            if 'users' in existing_tables and 'blogs' in existing_tables:
                logger.info("All required tables exist")
                return True
            else:
                logger.warning(f"Missing tables: {set(['users', 'blogs']) - set(existing_tables)}")
                return False
                
    except Exception as e:
        logger.error(f"Failed to check migration status: {e}")
        return False


def rollback_migrations():
    """Rollback all migrations (DANGEROUS - use only in development)."""
    try:
        with engine.connect() as connection:
            # Drop all tables
            connection.execute(text("DROP TABLE IF EXISTS blogs"))
            connection.execute(text("DROP TABLE IF EXISTS users"))
            connection.commit()
            
        logger.warning("All database tables dropped")
        
    except Exception as e:
        logger.error(f"Rollback failed: {e}")
        raise
