import os
import typer
import uvicorn
from app.db.migrations import migrate

cli = typer.Typer()

@cli.command()
def server():
    """Run the HTTP server."""
    port = int(os.getenv("HTTP_PORT", 8000))  # Default to port 8000 if HTTP_PORT is not set
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

@cli.command()
def migrate_up(steps: int = None):
    """Run database migrations up."""
    migrate('up', steps)
    typer.echo("Migrations completed.")

@cli.command()
def migrate_down(steps: int = None):
    """Run database migrations down."""
    migrate('down', steps)
    typer.echo("Migrations reverted.")

if __name__ == "__main__":
    cli()
