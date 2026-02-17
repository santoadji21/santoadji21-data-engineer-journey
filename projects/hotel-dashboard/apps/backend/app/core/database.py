import duckdb

from app.core.config import DUCKDB_PATH

_connection: duckdb.DuckDBPyConnection | None = None


def init_db() -> None:
    """Initialize the DuckDB connection."""
    global _connection
    _connection = duckdb.connect(DUCKDB_PATH, read_only=True)


def get_db() -> duckdb.DuckDBPyConnection:
    """Get the active DuckDB connection."""
    if _connection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _connection


def close_db() -> None:
    """Close the DuckDB connection."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
