# Trivia AI Playground - Docker Management Script
# PowerShell script for managing Docker containers on Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Trivia AI Playground - Docker Management" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  build          - Build the Docker images" -ForegroundColor Green
    Write-Host "  up             - Start all services (detached)" -ForegroundColor Green
    Write-Host "  up-build       - Build and start all services" -ForegroundColor Green
    Write-Host "  down           - Stop all services" -ForegroundColor Green
    Write-Host "  logs           - View logs from all services" -ForegroundColor Green
    Write-Host "  logs-postgres  - View PostgreSQL logs only" -ForegroundColor Green
    Write-Host "  logs-ingestion - View ingestion logs only" -ForegroundColor Green
    Write-Host "  clean          - Stop services and remove volumes (WARNING: deletes data!)" -ForegroundColor Green
    Write-Host "  restart        - Restart all services" -ForegroundColor Green
    Write-Host "  verify         - Show database statistics" -ForegroundColor Green
    Write-Host "  psql           - Connect to PostgreSQL with psql" -ForegroundColor Green
    Write-Host "  backup         - Backup database to backup.sql" -ForegroundColor Green
    Write-Host "  restore        - Restore database from backup.sql" -ForegroundColor Green
    Write-Host "  status         - Show status of all containers" -ForegroundColor Green
    Write-Host "  run-fresh      - Clean, rebuild, and start everything fresh" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\docker-manage.ps1 <command>" -ForegroundColor Yellow
    Write-Host "Example: .\docker-manage.ps1 up-build" -ForegroundColor Gray
}

function Build-Images {
    Write-Host "Building Docker images..." -ForegroundColor Cyan
    docker-compose build
}

function Start-Services {
    Write-Host "Starting all services..." -ForegroundColor Cyan
    docker-compose up -d
    Write-Host "Services started! Use '.\docker-manage.ps1 logs' to view logs" -ForegroundColor Green
}

function Start-ServicesBuild {
    Write-Host "Building and starting all services..." -ForegroundColor Cyan
    docker-compose up --build -d
    Start-Sleep -Seconds 3
    Write-Host "Services started! Use '.\docker-manage.ps1 logs' to view logs" -ForegroundColor Green
}

function Stop-Services {
    Write-Host "Stopping all services..." -ForegroundColor Cyan
    docker-compose down
    Write-Host "Services stopped!" -ForegroundColor Green
}

function Show-Logs {
    Write-Host "Showing logs (press Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f
}

function Show-PostgresLogs {
    Write-Host "Showing PostgreSQL logs (press Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f postgres
}

function Show-IngestionLogs {
    Write-Host "Showing ingestion logs (press Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f data_ingestion
}

function Clean-All {
    Write-Host "WARNING: This will delete all database data!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (yes/no)"
    if ($confirm -eq "yes") {
        Write-Host "Cleaning all services and volumes..." -ForegroundColor Cyan
        docker-compose down -v
        Write-Host "Cleaned successfully!" -ForegroundColor Green
    } else {
        Write-Host "Cancelled." -ForegroundColor Yellow
    }
}

function Restart-Services {
    Write-Host "Restarting all services..." -ForegroundColor Cyan
    docker-compose restart
    Write-Host "Services restarted!" -ForegroundColor Green
}

function Verify-Data {
    Write-Host "Verifying database data..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Total records:" -ForegroundColor Yellow
    docker exec -it trivia_postgres psql -U postgres -d trivia_db -c "SELECT COUNT(*) FROM trivia_questions;"
    Write-Host ""
    Write-Host "Records by value:" -ForegroundColor Yellow
    docker exec -it trivia_postgres psql -U postgres -d trivia_db -c "SELECT value, COUNT(*) as count FROM trivia_questions GROUP BY value ORDER BY value;"
}

function Connect-Psql {
    Write-Host "Connecting to PostgreSQL..." -ForegroundColor Cyan
    Write-Host "Type '\q' to exit psql" -ForegroundColor Gray
    docker exec -it trivia_postgres psql -U postgres -d trivia_db
}

function Backup-Database {
    Write-Host "Backing up database..." -ForegroundColor Cyan
    docker exec trivia_postgres pg_dump -U postgres trivia_db > backup.sql
    Write-Host "Database backed up to backup.sql" -ForegroundColor Green
}

function Restore-Database {
    if (Test-Path "backup.sql") {
        Write-Host "Restoring database from backup.sql..." -ForegroundColor Cyan
        Get-Content backup.sql | docker exec -i trivia_postgres psql -U postgres trivia_db
        Write-Host "Database restored!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: backup.sql not found!" -ForegroundColor Red
    }
}

function Show-Status {
    Write-Host "Container status:" -ForegroundColor Cyan
    docker-compose ps
}

function Run-Fresh {
    Write-Host "Running fresh setup..." -ForegroundColor Cyan
    Clean-All
    Start-ServicesBuild
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    Verify-Data
}

# Main command router
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "build" { Build-Images }
    "up" { Start-Services }
    "up-build" { Start-ServicesBuild }
    "down" { Stop-Services }
    "logs" { Show-Logs }
    "logs-postgres" { Show-PostgresLogs }
    "logs-ingestion" { Show-IngestionLogs }
    "clean" { Clean-All }
    "restart" { Restart-Services }
    "verify" { Verify-Data }
    "psql" { Connect-Psql }
    "backup" { Backup-Database }
    "restore" { Restore-Database }
    "status" { Show-Status }
    "run-fresh" { Run-Fresh }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
