import typer
import uvicorn
from app.db.migrations import migrate

cli = typer.Typer()


@cli.command()
def server():
    """Run the HTTP server."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


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
