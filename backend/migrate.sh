#!/bin/bash
# Database migration helper script for production

set -e

DB_URL="${DATABASE_URL:-postgresql+asyncpg://autofilm:autofilm@localhost:5432/autofilm}"
SYNC_DB_URL=$(echo "$DB_URL" | sed 's/sqlite+aiosqlite:\/\//sqlite:\/\//g' | sed 's/postgresql+asyncpg:\/\//postgresql+psycopg:\/\//g')

echo "🗄️  Database Migration Helper"
echo "Database URL: $SYNC_DB_URL"
echo ""

case "${1:-status}" in
    upgrade)
        echo "📤 Running database migrations (upgrade)..."
        alembic upgrade head
        echo "✅ Migrations applied successfully"
        ;;
    downgrade)
        if [ -z "$2" ]; then
            echo "❌ Error: downgrade requires a revision number"
            echo "Usage: $0 downgrade <revision>"
            exit 1
        fi
        echo "⬇️  Downgrading to revision $2..."
        alembic downgrade "$2"
        echo "✅ Downgrade completed"
        ;;
    rollback)
        echo "⬅️  Rolling back last migration..."
        alembic downgrade -1
        echo "✅ Rollback completed"
        ;;
    status)
        echo "📊 Migration status:"
        alembic current
        echo ""
        echo "📝 Available revisions:"
        alembic history --oneline
        ;;
    generate)
        if [ -z "$2" ]; then
            echo "❌ Error: generate requires a migration name"
            echo "Usage: $0 generate <migration_name>"
            exit 1
        fi
        echo "🔨 Generating migration: $2..."
        alembic revision --autogenerate -m "$2"
        echo "✅ Migration created in alembic/versions/"
        ;;
    *)
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  upgrade              Apply all pending migrations"
        echo "  downgrade <rev>      Revert to specific revision"
        echo "  rollback             Revert last migration"
        echo "  status               Show current migration status"
        echo "  generate <name>      Create new migration (autogenerate from models)"
        echo ""
        exit 1
        ;;
esac
