import os
import shutil
from pathlib import Path

import orjson


def load_json(path: str | Path, allow_empty: bool = False) -> dict:
    if allow_empty and not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return orjson.loads(f.read())


def save_json(path: str | Path, data: dict):
    with open(path, "wb") as f:
        f.write(
            orjson.dumps(
                data,
                option=orjson.OPT_SORT_KEYS
                + orjson.OPT_SERIALIZE_NUMPY
                + orjson.OPT_APPEND_NEWLINE
                + orjson.OPT_NON_STR_KEYS,
            )
        )


def save(path: str, data: str):
    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(data)


def load(path: str) -> str:
    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:
        return f.read()


def from_current_file(path: str) -> Path:
    dirname = os.path.dirname(__file__)
    return Path(os.path.join(dirname, path))


def remove_path(path: str | Path):
    shutil.rmtree(path, ignore_errors=True)
    try:
        os.remove(path)
    except OSError:
        pass
