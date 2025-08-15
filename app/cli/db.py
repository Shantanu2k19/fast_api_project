"""
CLI tool for database management.
"""
import click
import logging
from app.core.migrations import (
    run_migrations, 
    check_migration_status, 
    rollback_migrations
)
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@click.group()
def db():
    """Database management commands."""
    pass


@db.command()
def init():
    """Initialize database with all tables and indexes."""
    click.echo("Initializing database...")
    try:
        run_migrations()
        click.echo("✅ Database initialized successfully!")
    except Exception as e:
        click.echo(f"❌ Database initialization failed: {e}")
        raise click.Abort()


@db.command()
def status():
    """Check database migration status."""
    click.echo("Checking database status...")
    try:
        if check_migration_status():
            click.echo("✅ Database is up to date!")
        else:
            click.echo("⚠️  Database needs migration!")
    except Exception as e:
        click.echo(f"❌ Failed to check status: {e}")
        raise click.Abort()


@db.command()
@click.option('--force', is_flag=True, help='Force rollback without confirmation')
def rollback(force):
    """Rollback all migrations (DANGEROUS - use only in development)."""
    if not force:
        if not click.confirm("This will delete ALL data. Are you sure?"):
            click.echo("Rollback cancelled.")
            return
    
    click.echo("Rolling back database...")
    try:
        rollback_migrations()
        click.echo("✅ Database rolled back successfully!")
    except Exception as e:
        click.echo(f"❌ Rollback failed: {e}")
        raise click.Abort()


@db.command()
def reset():
    """Reset database (drop all tables and recreate)."""
    if not click.confirm("This will delete ALL data. Are you sure?"):
        click.echo("Reset cancelled.")
        return
    
    click.echo("Resetting database...")
    try:
        rollback_migrations()
        run_migrations()
        click.echo("✅ Database reset successfully!")
    except Exception as e:
        click.echo(f"❌ Reset failed: {e}")
        raise click.Abort()


if __name__ == '__main__':
    db()
