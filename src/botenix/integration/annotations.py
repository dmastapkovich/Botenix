from collections.abc import Mapping, Sequence
from typing import IO, Any, Literal


PrimitiveData = str | int | float | bool | None

RequestQueryParam = (
    Mapping[str, PrimitiveData | Sequence[PrimitiveData]]
    | list[tuple[str, PrimitiveData]]
    | tuple[tuple[str, PrimitiveData], ...]
    | str
    | bytes
)

RequestJson = Mapping[str, Any] | str | bytes
SerializedJson = Mapping[str, Any] | list[Any]

FileContent = IO[bytes] | bytes | str
FileTypes = (
    FileContent
    | tuple[str | None, FileContent]
    | tuple[str | None, FileContent, str | None]
    | tuple[str | None, FileContent, str | None, Mapping[str, str]]
)
RequestFiles = Mapping[str, FileTypes] | Sequence[tuple[str, FileTypes]]

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
IncEx = set[int] | set[str] | Mapping[int, Any] | Mapping[str, Any]
