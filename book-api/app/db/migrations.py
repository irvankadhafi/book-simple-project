import os
from sqlalchemy.sql import text
from app.db.postgresql import engine, Base
from app.config.config import config


def execute_sql_file(connection, file_path):
    with open(file_path, 'r') as f:
        sql = f.read()

    # Split the SQL file into 'up' and 'down' parts
    parts = sql.split('-- +migrate Down')
    up_sql = parts[0].split('-- +migrate Up')[1].strip()
    down_sql = parts[1].strip() if len(parts) > 1 else ''

    return up_sql, down_sql


def get_migration_files():
    migration_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'migrations')
    return sorted([f for f in os.listdir(migration_dir) if f.endswith('.sql')])


def create_migrations_table(connection):
    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """))


def get_applied_migrations(connection):
    result = connection.execute(text("SELECT name FROM migrations"))
    return set(row[0] for row in result)


def apply_migration(connection, file_name, sql):
    connection.execute(text(sql))
    connection.execute(text("INSERT INTO migrations (name) VALUES (:name)"), {"name": file_name})


def remove_migration(connection, file_name, sql):
    connection.execute(text(sql))
    connection.execute(text("DELETE FROM migrations WHERE name = :name"), {"name": file_name})


def migrate(direction='up', steps=None):
    with engine.begin() as connection:
        create_migrations_table(connection)
        applied_migrations = get_applied_migrations(connection)
        migration_files = get_migration_files()

        if direction == 'up':
            to_apply = [f for f in migration_files if f not in applied_migrations]
            if steps:
                to_apply = to_apply[:steps]
            for file_name in to_apply:
                file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'migrations', 'versions', file_name)
                up_sql, _ = execute_sql_file(connection, file_path)
                apply_migration(connection, file_name, up_sql)
                print(f"Applied migration: {file_name}")
        elif direction == 'down':
            to_remove = [f for f in reversed(migration_files) if f in applied_migrations]
            if steps:
                to_remove = to_remove[:steps]
            for file_name in to_remove:
                file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'migrations', 'versions', file_name)
                _, down_sql = execute_sql_file(connection, file_path)
                remove_migration(connection, file_name, down_sql)
                print(f"Reverted migration: {file_name}")
