import os
from pathlib import Path

DB_URL = os.getenv('DB_URL', 'sqlite://:memory:')


def get_root():
    current_file = Path(__file__)
    current_file_dir = current_file.parent
    project_root = current_file_dir.parent
    project_root_absolute = project_root.resolve()
    static_root_absolute = project_root_absolute / "static"
    return project_root_absolute, static_root_absolute
