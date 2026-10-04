"""Общие настройки базы данных."""

METADATA_FILE = "db_meta.json"
DATA_DIR = "data"

TYPE_MAP = {
    "int": int,
    "str": str,
    "bool": bool,
}

VALID_TYPES = set(TYPE_MAP)
