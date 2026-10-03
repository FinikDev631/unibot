from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Union


@dataclass
class FileUpload:
    data: bytes
    filename: str = "file"


def normalize_file(value: Union[str, Path, bytes, bytearray, BinaryIO, FileUpload]):
    if isinstance(value, FileUpload):
        return value.filename, value.data
    if isinstance(value, (str, Path)):
        path = Path(value)
        return path.name, path.read_bytes()
    if isinstance(value, bytes):
        return "file", value
    if isinstance(value, bytearray):
        return "file", bytes(value)
    if hasattr(value, "read"):
        data = value.read()
        name = getattr(value, "name", "file")
        return Path(str(name)).name, data
    raise TypeError("Unsupported file value")
