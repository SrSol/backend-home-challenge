import sys
from pathlib import Path
import click
from alembic import command
from alembic.config import Config

# Validate if src is in the path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.shared.infrastructure.config.settings import get_settings

def get_alembic_config():
    """Get Alembic config with correct database URL"""
    settings = get_settings()
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    return alembic_cfg

@click.group()
def cli():
    """Database management commands"""
    pass

@cli.command()
def init():
    """Initialize database with all migrations"""
    try:
        click.echo("Initializing database...")
        cfg = get_alembic_config()
        command.upgrade(cfg, "head")
        click.echo("✅ Database initialized successfully")
    except Exception as e:
        click.echo(f"❌ Error initializing database: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('name')
def create_migration(name: str):
    """Create a new migration"""
    try:
        cfg = get_alembic_config()
        revision = command.revision(
            cfg,
            message=name,
            autogenerate=True
        )
        click.echo(f"✅ Created migration: {revision.revision}")
    except Exception as e:
        click.echo(f"❌ Error creating migration: {e}", err=True)
        sys.exit(1)

@cli.command()
def upgrade():
    """Apply all pending migrations"""
    try:
        cfg = get_alembic_config()
        command.upgrade(cfg, "head")
        click.echo("✅ Applied all pending migrations")
    except Exception as e:
        click.echo(f"❌ Error applying migrations: {e}", err=True)
        sys.exit(1)

@cli.command()
def downgrade():
    """Revert last migration"""
    try:
        cfg = get_alembic_config()
        command.downgrade(cfg, "-1")
        click.echo("✅ Reverted last migration")
    except Exception as e:
        click.echo(f"❌ Error reverting migration: {e}", err=True)
        sys.exit(1)

@cli.command()
def status():
    """Show current migration status"""
    try:
        cfg = get_alembic_config()
        command.current(cfg, verbose=True)
    except Exception as e:
        click.echo(f"❌ Error getting status: {e}", err=True)
        sys.exit(1)

@cli.command()
def reset():
    """Reset database (WARNING: destroys all data)"""
    if click.confirm('⚠️  This will delete all data. Are you sure?'):
        try:
            cfg = get_alembic_config()
            command.downgrade(cfg, "base")
            command.upgrade(cfg, "head")
            click.echo("✅ Database reset successfully")
        except Exception as e:
            click.echo(f"❌ Error resetting database: {e}", err=True)
            sys.exit(1)

if __name__ == '__main__':
    cli()
