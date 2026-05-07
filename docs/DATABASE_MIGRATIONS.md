# Database Management Guide

## Overview

This project uses **Alembic** for database schema management. All database changes must be handled through migrations, never through automatic schema creation.

## Key Principles

1. **Migrations are version-controlled**: All schema changes are tracked in `alembic/versions/`
2. **Single source of truth**: Database schema is defined by migrations, not by Python models
3. **Rollback capability**: Every migration should be reversible
4. **Production safety**: Migrations are carefully reviewed before deployment

## Quick Start

### Prerequisites

```bash
# Ensure dependencies are installed
poetry install

# Set database URL (PostgreSQL recommended for production)
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/autofilm"
```

### Common Tasks

#### Apply all pending migrations
```bash
# Linux/macOS
./migrate.sh upgrade

# Windows
migrate.bat upgrade

# Or directly with Alembic
alembic upgrade head
```

#### Check migration status
```bash
./migrate.sh status
alembic current  # Current schema version
alembic history  # All migration history
```

#### Create a new migration after model changes
```bash
# Auto-generate from model changes
./migrate.sh generate "add_new_field"

# Review generated migration in alembic/versions/
# Edit if needed for complex changes
```

#### Rollback last migration
```bash
./migrate.sh rollback
alembic downgrade -1
```

#### Rollback to specific version
```bash
./migrate.sh downgrade 20260424_0001
alembic downgrade <revision_id>
```

## Migration Workflow

### For Developers

1. **Modify Python models** in `app/models/`
2. **Generate migration**:
   ```bash
   alembic revision --autogenerate -m "descriptive_name"
   ```
3. **Review generated migration** in `alembic/versions/`
4. **Test locally**:
   ```bash
   alembic upgrade head
   ```
5. **Test rollback**:
   ```bash
   alembic downgrade -1
   alembic upgrade head
   ```
6. **Commit migration file** to version control

### For Production Deployment

1. **Backup database** before any migration
2. **Run migration**:
   ```bash
   alembic upgrade head
   ```
3. **Verify deployment**:
   ```bash
   alembic current
   ```
4. **Keep database backup** for 7+ days

## Migration Best Practices

### DO ✅

- Write migrations that can be reversed (reversible)
- Use descriptive migration names
- Test migrations locally before committing
- Backup production database before migrations
- Keep migrations small and focused
- Use timeouts for long-running migrations

### DON'T ❌

- Don't use `create_all()` - use migrations instead
- Don't delete migration files after they're committed
- Don't modify migrations that are already deployed
- Don't skip migration steps in production
- Don't run migrations during business hours without maintenance window

## Common Migration Patterns

### Adding a new table
```python
def upgrade() -> None:
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('new_table')
```

### Adding a column
```python
def upgrade() -> None:
    op.add_column('users', sa.Column('new_field', sa.String(100)))

def downgrade() -> None:
    op.drop_column('users', 'new_field')
```

### Adding a unique constraint
```python
def upgrade() -> None:
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

def downgrade() -> None:
    op.drop_constraint('uq_users_email', 'users', type_='unique')
```

## Troubleshooting

### Migration fails locally
```bash
# Reset to clean state (DEV ONLY!)
alembic downgrade base
# Or check database connection
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/autofilm"
alembic current
```

### Migrations out of sync with models
```bash
# Generate corrective migration
alembic revision --autogenerate -m "fix_schema_sync"
```

### Can't find migration ID
```bash
# List all revisions
alembic history

# Current state
alembic current
```

## Database Backup/Restore

### PostgreSQL Backup
```bash
pg_dump -U autofilm -d autofilm > backup.sql
```

### PostgreSQL Restore
```bash
psql -U autofilm -d autofilm < backup.sql
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
