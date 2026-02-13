import sqlite3
from pathlib import Path

def get_connection():
    """
    Returns a connection to the SQLite database 'tennis_db.sqlite'.
    Make sure 'tennis_db.sqlite' is in the project root folder.
    """
    # Path to SQLite DB in project root
    db_path = Path(__file__).parent.parent / "tennis_db.sqlite"

    # Create connection
    conn = sqlite3.connect(db_path)
    return conn
