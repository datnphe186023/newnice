@echo off
REM Database migration helper script for Windows

setlocal enabledelayedexpansion

if "%DATABASE_URL%"=="" (
    set "DB_URL=postgresql+asyncpg://autofilm:autofilm@localhost:5432/autofilm"
) else (
    set "DB_URL=%DATABASE_URL%"
)

echo.
echo ====== Database Migration Helper ======
echo Database: %DB_URL%
echo.

set "COMMAND=%1"
if "%COMMAND%"=="" set "COMMAND=status"

if "%COMMAND%"=="upgrade" (
    echo Running database migrations (upgrade)...
    alembic upgrade head
    echo ✓ Migrations applied successfully
    goto :end
)

if "%COMMAND%"=="downgrade" (
    if "%2"=="" (
        echo Error: downgrade requires a revision number
        echo Usage: migrate.bat downgrade ^<revision^>
        goto :end
    )
    echo Downgrading to revision %2...
    alembic downgrade %2
    echo ✓ Downgrade completed
    goto :end
)

if "%COMMAND%"=="rollback" (
    echo Rolling back last migration...
    alembic downgrade -1
    echo ✓ Rollback completed
    goto :end
)

if "%COMMAND%"=="status" (
    echo Migration status:
    alembic current
    echo.
    echo Available revisions:
    alembic history --oneline
    goto :end
)

if "%COMMAND%"=="generate" (
    if "%2"=="" (
        echo Error: generate requires a migration name
        echo Usage: migrate.bat generate ^<migration_name^>
        goto :end
    )
    echo Generating migration: %2...
    alembic revision --autogenerate -m "%2"
    echo ✓ Migration created in alembic/versions/
    goto :end
)

echo Usage: migrate.bat ^<command^> [args]
echo.
echo Commands:
echo   upgrade              Apply all pending migrations
echo   downgrade ^<rev^>     Revert to specific revision
echo   rollback             Revert last migration
echo   status               Show current migration status
echo   generate ^<name^>     Create new migration (autogenerate from models)

:end
endlocal
